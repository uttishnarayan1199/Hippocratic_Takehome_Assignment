#Hippocratic Bedtime Story Agent

This project is my solution to the Hippocratic AI coding assignment.

It implements a small multi-agent system that:
- Generates bedtime stories for children aged 5–10.
- Uses a separate **LLM judge** to score safety, simplicity, and tone.
- Iteratively **revises** the story if it does not meet a quality threshold.
- Lets the user **request additional changes** (e.g., “make it shorter”, “more funny”).
- Categorizes the user’s request (soothing / adventure / funny / learning / sensitive / general)
  and adapts the story style accordingly.

The OpenAI model is **gpt-3.5-turbo**, as required.

---

## Project Structure

- `main.py`  
  Command-line entrypoint. Orchestrates the flow:
  1. Get story request from user  
  2. Generate story  
  3. Judge the story  
  4. Optionally revise in a loop  
  5. Optionally apply user feedback

- `utils.py`  
  - Wraps the OpenAI client and chat completion call.  
  - Loads `OPENAI_API_KEY` from `.env`.  
  - Provides a simple `call_chat_model()` helper.

- `prompts.py`  
  - Contains system prompts for:
    - Story generator (storyteller)
    - Judge
    - Revision agent

- `storyteller.py`  
  - `categorize_request()` → classifies the request into categories like “soothing”, “adventure”, etc.  
  - `generate_initial_story()` → generates the first draft using category-specific guidance.  
  - `revise_story()` → rewrites the story based on judge feedback and optional user feedback.

- `judge.py`  
  - `judge_story()` → calls the judge LLM with a strict JSON schema.  
  - `is_good_enough()` → decides if the story passes the threshold.

---

## Architecture

High-level flow:

```text
User
  |
  v
main.py  ──────────────────────────────────────────────────────────────┐
  |                                                                    |
  | 1. Read user request                                               |
  v                                                                    |
categorize_request()  (storyteller.py)                                 |
  |                                                                    |
  v                                                                    |
generate_initial_story()  ──>  initial story                           |
  |                                                                    |
  v                                                                    |
judge_story()  (judge.py) ──> scores + feedback                        |
  |                                                                    |
  | if not good enough (score too low)                                 |
  v                                                                    |
revise_story()  (storyteller.py) <─────── judge feedback               |
  |                           (loop max N times)                       |
  └────────────────────────────────────────────────────────────────────┘

After the automated loop:

User feedback (optional, e.g. "more funny", "shorter")
  |
  v
revise_story(..., user_feedback=...)  ──> updated story
  |
  v
judge_story()  ──> final scores
