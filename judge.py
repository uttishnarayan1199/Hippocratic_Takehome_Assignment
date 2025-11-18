"""
Story quality and safety judge.

This module turns the LLM into a critic that:
- scores a story along multiple dimensions, and
- suggests specific improvements.

The output is machine-readable JSON so the orchestrator can decide
whether to accept the story or trigger a revision loop.
"""

import json
from typing import Dict, Any

from utils import call_chat_model
from prompts import JUDGE_SYSTEM_PROMPT


def _parse_json_safely(raw: str) -> Dict[str, Any]:
    """
    Try to parse JSON from the model's response.

    Even though we tell the model to return strict JSON, LLMs sometimes
    add extra text. This helper:
    - first tries json.loads directly,
    - then tries to extract the first {...} block if that fails.
    """
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Try to extract a JSON object from within the text
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start == -1 or end == 0:
            raise ValueError(f"Could not find JSON in judge response: {raw}")
        json_str = raw[start:end]
        return json.loads(json_str)


def judge_story(user_request: str, story: str) -> Dict[str, Any]:
    """
    Ask the judge LLM to evaluate a story.

    Inputs:
    - user_request: the original story request
    - story: the generated story

    Output:
    - a dict with numeric scores and improvement suggestions, e.g.
      {
        "age_appropriateness": 9,
        "clarity_and_coherence": 8,
        "emotional_tone": 9,
        "creativity": 8,
        "language_simplicity": 9,
        "overall_score": 9,
        "improvements": ["...", "..."]
      }
    """
    messages = [
        {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                "Here is the original bedtime story request:\n"
                f"{user_request}\n\n"
                "Here is the story that was generated:\n"
                f"{story}\n\n"
                "Please evaluate this story according to your instructions and "
                "return ONLY the JSON result."
            ),
        },
    ]

    # Lower temperature: we want consistent, deterministic-ish judgments.
    raw_response = call_chat_model(messages, max_tokens=800, temperature=0.2)
    result = _parse_json_safely(raw_response)
    return result


def is_good_enough(judge_result: Dict[str, Any], threshold: int = 8) -> bool:
    """
    Decide whether a story is acceptable based on the overall_score.

    Default threshold is 8/10, but this can be tuned.

    Keeping this logic in a helper function makes it trivial to experiment
    with different thresholds or combine multiple criteria later.
    """
    overall = judge_result.get("overall_score")
    try:
        return int(overall) >= threshold
    except (TypeError, ValueError):
        # If something is wrong with the score, be conservative and say "not good enough".
        return False
