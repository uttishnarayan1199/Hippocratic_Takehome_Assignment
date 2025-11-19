Hippocratic Bedtime Story Agent

A safe, multi-agent storytelling pipeline designed for the Hippocratic AI Take-Home Assignment

This project implements a multi-step, safety-aligned storytelling system that generates child-appropriate bedtime stories using a structured agent workflow.
Each story is produced, evaluated, revised, and optionally refined based on user feedback—ensuring every output is safe, gentle, and suitable for children.

Overview

The system uses three coordinated agents:

1. Story Generator Agent

Produces the initial bedtime story

Tailors tone and style based on request category

Ensures the story is gentle and suitable for young readers

2. Judge Agent

Evaluates the story on multiple criteria:

Age appropriateness

Emotional tone

Clarity & coherence

Creativity

Language simplicity

Returns a structured JSON score and suggested improvements.

3. Reviser Agent

Improves the story using judge feedback

Ensures safety guidelines are met

Iterates up to two times to reach a minimum quality threshold

Optional: User Feedback Loop

After automated revisions, users may request additional refinements (e.g., “make it funnier,” “shorter,” “more magical”).
The reviser incorporates the feedback while maintaining safety constraints.

Project Structure
.
├── main.py               # Main entry point: coordinates the agent loop
├── storyteller.py        # Story generator + revision logic
├── judge.py              # Evaluation and scoring logic
├── prompts.py            # Centralized prompt templates
├── utils.py              # OpenAI client wrapper, env loader, helpers
├── README.md
└── requirements.txt

How It Works (Pipeline Flow)

User Request
User describes the bedtime story they want.

Categorization
Request is categorized to apply the correct storytelling style.

Initial Story Generation
The Storyteller agent creates a first draft.

Judging & Scoring
The Judge agent returns:

multiple sub-scores

an overall score

improvement suggestions

Automated Revision Loop
If the story does not meet the threshold:

it is revised

evaluated again

loop repeats (max 2 iterations)

Optional User Feedback
User may ask for adjustments (tone, length, humor, etc.).
Story is rewritten while preserving safety.

Final Story Output

Running the Project
1. Clone the repository
git clone https://github.com/uttishnarayan1199/Hippocratic_Takehome_Assignment.git
cd Hippocratic_Takehome_Assignment

2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Create a .env file

In the project root, create a file named .env:

OPENAI_API_KEY=sk-proj-xxxxxx


(Your key must be added manually. None are included in this repository.)

5. Run the agent
python main.py


You will be prompted:

=== Hippocratic Bedtime Story Generator ===
Describe the kind of bedtime story you want:


Enter any request—for example:

A bedtime story about a little rabbit who wants to reach the stars


The full cycle (Draft → Judge → Revise → Feedback) will run automatically.

Safety & Design Considerations

This agent is built with strict safety controls to meet Hippocratic AI guidelines:

No violence, weapons, or fear-inducing elements

No emotionally heavy or adult themes

Language tuned for children aged 5–10

Clear, gentle, emotionally stable tone

Automatic rewriting to enforce safety rules

The Judge agent heavily penalizes:

frightening or intense imagery

inappropriate emotional content

complex vocabulary

abstract or psychologically heavy ideas

Stories are continually revised until safe.

Technical Design Highlights

Modular Architecture
Each agent (storyteller, judge, reviser) resides in its own module for clarity.

Centralized Prompt Management
All prompt templates live in prompts.py for easy iteration and fine-tuning.

Unified OpenAI Wrapper
call_chat_model() in utils.py abstracts away model calls.

Clear, Single Entry Point
main.py orchestrates the full agent pipeline.

Configurable Threshold Logic
The evaluation strictness can be adjusted in is_good_enough().

Dependencies

Listed in requirements.txt:

openai>=1.0.0
python-dotenv

Notes for Reviewers

No API keys are included in this repository.

.env must be created by the user.

Code is clean, modular, and easy to audit.

The system runs end-to-end with a single command:

python main.py
