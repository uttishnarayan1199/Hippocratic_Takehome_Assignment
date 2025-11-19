💤 Hippocratic Bedtime Story Agent

A safe, multi-agent storytelling system designed for the Hippocratic AI Take-Home Assignment.

This project implements a multi-step, safety-aligned pipeline that generates child-appropriate bedtime stories using LLM agents. Every story is generated, judged, revised, and optionally refined using user feedback—ensuring all outputs remain safe, gentle, and developmentally appropriate.

✨ Overview

The system is built around three coordinated agents, orchestrated through a structured pipeline.

1. Story Generator Agent

Produces the initial bedtime story

Adapts tone/style based on request category

Ensures a soft, gentle, child-friendly narrative

2. Judge Agent

Evaluates the story across multiple criteria:

Age appropriateness

Emotional tone

Clarity & coherence

Creativity

Language simplicity

Returns:

A structured JSON evaluation

Suggested improvements for revision

3. Reviser Agent

Improves the story using judge feedback

Keeps safety and emotional tone within guidelines

Can incorporate optional user feedback (e.g., “make it funnier”, “shorter”)

▶️ How to Run the Project
1. Clone the repository
git clone https://github.com/uttishnarayan1199/Hippocratic_Takehome_Assignment.git
cd Hippocratic_Takehome_Assignment

2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Add your API key

Create .env in the project root:

OPENAI_API_KEY=sk-proj-xxxxxx

5. Run the agent
python main.py


You will see:

=== Hippocratic Bedtime Story Generator ===
Describe the kind of bedtime story you want:


Enter any prompt such as:

A story about a sleepy panda who learns to be brave

The system will:

Generate → Judge → Revise

Ask if you want extra modifications

Output a safe final story

🔒 Safety Design

This project follows child-safety guidelines:

No violence

No frightening scenarios

No intense emotional themes

No mature or abstract concepts

Simple language suitable for ages 5–10

The Judge Agent enforces these rules with scoring penalties and required revisions.

🛠️ Technical Design Notes

Modular architecture: agents separated into clear modules

Centralized prompt management for easier tuning

Strict OpenAI wrapper ensuring consistent API calls

Configurable scoring threshold in is_good_enough()

User feedback loop maintains safety before applying modifications

📦 Requirements

requirements.txt includes:

openai>=1.0.0

python-dotenv

📝 Notes for Reviewers

No API keys are committed (intentionally).

.env must be created locally.

Project is fully runnable with one command:

python main.py


Code is easy to extend, refactor, and maintain.
