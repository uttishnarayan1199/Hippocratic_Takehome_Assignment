"""
Story generation and revision logic.

This module uses:
- STORYTELLER_SYSTEM_PROMPT for initial story creation.
- REVISION_SYSTEM_PROMPT for story refinement based on judge feedback
  and optional user feedback.
"""

from typing import Dict, Any, Optional

from utils import call_chat_model
from prompts import STORYTELLER_SYSTEM_PROMPT, REVISION_SYSTEM_PROMPT


# --- NEW: simple rule-based categorizer ------------------------


def categorize_request(user_request: str) -> str:
    """
    Very lightweight classifier for the user's request.

    Categories:
    - "soothing": very calm, sleepy, gentle bedtime themes
    - "adventure": quests, journeys, dragons, exploring
    - "funny": silly, jokes, playful chaos
    - "learning": explicit "teach", "lesson", "moral", "learn"
    - "sensitive": divorce, death, ghosts, war, scary stuff
    - "general": everything else

    The goal is not perfect classification, but to steer the generator
    toward a slightly different tone/structure depending on the request.
    """
    text = user_request.lower()

    if any(word in text for word in ["sleep", "calm", "relax", "goodnight", "soothing"]):
        return "soothing"
    if any(word in text for word in ["adventure", "quest", "journey", "explore", "dragon", "pirate"]):
        return "adventure"
    if any(word in text for word in ["funny", "silly", "joke", "hilarious", "laugh"]):
        return "funny"
    if any(word in text for word in ["teach", "learn", "lesson", "moral", "value", "kindness", "sharing"]):
        return "learning"
    if any(
        word in text
        for word in [
            "divorce",
            "death",
            "dead",
            "ghost",
            "haunted",
            "monster",
            "war",
            "battle",
            "kill",
            "murder",
            "scary",
            "afraid",
        ]
    ):
        return "sensitive"

    return "general"


# --- Story generation ------------------------------------------


def generate_initial_story(user_request: str) -> str:
    """
    Generate a first-draft bedtime story from the user's request.

    Now also:
    - Categorizes the request.
    - Passes category-specific guidance to the model.
    """
    category = categorize_request(user_request)

    category_instructions = {
        "soothing": "Use an extra calm, sleepy tone with very gentle pacing and short, simple sentences.",
        "adventure": "Include a light, low-stakes adventure, but keep everything safe, non-violent, and reassuring.",
        "funny": "Add light, child-friendly humor and silly moments, but avoid sarcasm or anything mean-spirited.",
        "learning": "Emphasize a clear, simple lesson or moral, but keep the story fun and not preachy.",
        "sensitive": (
            "The user's request touches on sensitive or potentially scary themes. "
            "Transform it into a completely safe, gentle, age-appropriate story. "
            "Remove heavy topics (e.g. divorce, death, war, ghosts that scare children) and "
            "replace them with comforting, child-friendly situations."
        ),
        "general": "Default to a kind, gentle, age-appropriate bedtime tone.",
    }

    extra_guidance = category_instructions.get(category, category_instructions["general"])

    messages = [
        {"role": "system", "content": STORYTELLER_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                "You are generating a bedtime story for a child aged 5–10.\n\n"
                f"Detected request category: {category}\n"
                f"Category-specific guidance: {extra_guidance}\n\n"
                "Here is the bedtime story request from a parent or child:\n"
                f"{user_request}\n\n"
                "Please write a complete bedtime story that follows the global guidelines "
                "AND the category-specific guidance."
            ),
        },
    ]

    story = call_chat_model(messages, max_tokens=1200, temperature=0.8)
    return story


# --- Story revision --------------------------------------------


def revise_story(
    user_request: str,
    previous_story: str,
    judge_feedback: Dict[str, Any],
    user_feedback: Optional[str] = None,
) -> str:
    """
    Revise an existing story based on structured judge feedback
    and optional direct user feedback.

    Inputs:
    - user_request: the original request ("a story about...")
    - previous_story: the last version of the story
    - judge_feedback: dict with scores + improvement suggestions
    - user_feedback: optional free-text feedback from the user such as
      "make it shorter" or "focus more on the dragon"

    Output:
    - an improved story as plain text
    """
    # Build the main content for the revision request
    content = (
        "Here is the original bedtime story request:\n"
        f"{user_request}\n\n"
        "Here is the previous version of the story:\n"
        f"{previous_story}\n\n"
        "Here is structured feedback from the story judge as JSON:\n"
        f"{judge_feedback}\n\n"
        "Please rewrite the story to address ALL of the judge's feedback while "
        "keeping the story appropriate for children aged 5–10."
    )

    if user_feedback:
        content += (
            "\n\nHere is additional feedback directly from the user about how to change the story:\n"
            f"{user_feedback}\n\n"
            "You MUST incorporate the user's feedback as long as it remains safe and age-appropriate."
        )

    messages = [
        {"role": "system", "content": REVISION_SYSTEM_PROMPT},
        {"role": "user", "content": content},
    ]

    revised_story = call_chat_model(messages, max_tokens=1200, temperature=0.7)
    return revised_story
