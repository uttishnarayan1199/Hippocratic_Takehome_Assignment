🚀 Hippocratic Bedtime Story Agent

A multi-agent storytelling system designed for the Hippocratic AI Take-Home Assignment

This project implements a safe, child-appropriate bedtime story generator using a multi-step agent workflow:

Story Generator Agent – writes a creative story based on user input

Judge Agent – evaluates the story’s safety, tone, age-appropriateness, and clarity

Reviser Agent – improves the story using judge feedback

Optional User Feedback Loop – user can request changes (e.g., “make it funnier”)

The system ensures every generated story is:

safe for children

emotionally appropriate

clear and coherent

aligned with Hippocratic AI’s guidelines

📁 Project Structure
.
├── main.py                # Entry point: handles the full Story → Judge → Revise loop
├── storyteller.py         # Story generator and revision agent
├── judge.py               # Story evaluator (safety, clarity, tone)
├── prompts.py             # Centralized prompt templates for agents
├── utils.py               # OpenAI client, environment loader, helper functions
├── README.md
└── requirements.txt

🧠 How It Works (Agent Workflow)
1. User Request

The user describes the kind of bedtime story they want.

2. Story Generator Agent

Produces an initial draft

Uses prompt templates tailored by story category

Ensures age-appropriate tone for children

3. Judge Agent

Evaluates the story on:

Age appropriateness

Emotional tone

Clarity & coherence

Creativity

Language simplicity

Returns a structured JSON score + list of improvements.

4. Revision Loop

If the story score is below a threshold:

The system revises the story using judge feedback

Runs another evaluation

Repeats for up to 2 iterations

5. Optional User Feedback

After the automated loop, the user can request further changes, e.g.:

make it shorter
make it funnier
focus more on the dragon


The story is revised again while maintaining safety.

▶️ How to Run the Project
1. Clone the repo
git clone https://github.com/uttishnarayan1199/Hippocratic_Takehome_Assignment.git
cd Hippocratic_Takehome_Assignment

2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Create a .env file

Create a file named .env in the project root:

OPENAI_API_KEY=sk-proj-xxxxx


(Use your own key — it is not included in this repo.)

5. Run the agent
python main.py


You will see:

=== Hippocratic Bedtime Story Generator ===
Describe the kind of bedtime story you want:


Enter your story request, such as:

A story about a little rabbit who wants to reach the stars


The agent will:

Generate a draft

Judge it

Revise it until safe

Ask if you want further changes

🔒 Safety Considerations

This agent includes strict guardrails to ensure stories remain:

non-violent

non-frightening

emotionally gentle

developmentally appropriate for ages 5–10

The judge prompt penalizes:

complex, abstract, or adult themes

fear-inducing imagery

emotionally heavy topics

excessive vocabulary complexity

Stories are rewritten automatically until safe.

🛠️ Technical Design Choices

Modular design
Each agent (storyteller, judge, reviser) is in its own file for clarity.

Centralized prompts
All prompt templates live in prompts.py for easy tuning.

Reusable OpenAI wrapper
utils.py provides a single call_chat_model() function abstracting model calls.

Clear entrypoint
main.py contains the full pipeline and makes the project easy to run.

User-adjustable revision threshold
You can tune the scorer’s strictness by editing is_good_enough().

📦 Dependencies

requirements.txt includes:

openai>=1.0.0
python-dotenv

📌 Notes for Reviewers

No API keys are committed (by design).

.env must be created manually.

Code is readable, modular, and easy to extend.

The project can be run entirely from main.py with one command.
