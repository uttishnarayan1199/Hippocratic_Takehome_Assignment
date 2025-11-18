"""
Command-line entrypoint for the Hippocratic bedtime story agent.

Flow:
1. Read a story request from the user.
2. Generate an initial story draft.
3. Have the judge evaluate it and return structured feedback.
4. If the story is not good enough (overall_score < threshold),
   iteratively revise and re-judge a small number of times.
5. Print the final story and a brief summary of judge scores.
6. Optionally let the user provide additional feedback and run
   one more revision pass tailored to that feedback.

This demonstrates an agent loop:
  Storyteller -> Judge -> (optional) Reviser -> Final Output
"""

from storyteller import generate_initial_story, revise_story
from judge import judge_story, is_good_enough


def run_story_loop():
    print("=== Hippocratic Bedtime Story Generator ===")
    print("Describe the kind of bedtime story you want.")
    user_request = input("Story request: ")

    # 1) Generate initial story
    print("\n[1/3] Generating initial story draft...\n")
    story = generate_initial_story(user_request)
    print("----- INITIAL STORY -----\n")
    print(story)

    # 2) Judge the story
    print("\n[2/3] Evaluating story quality and safety...\n")
    judge_result = judge_story(user_request, story)
    print("----- JUDGE RESULT -----")
    print(judge_result)

    # 3) Optionally improve story based on judge feedback
    max_iterations = 2
    iteration = 0

    while not is_good_enough(judge_result) and iteration < max_iterations:
        iteration += 1
        print(f"\n[3/{3}] Story not good enough yet (iteration {iteration}).")
        print("Revising story based on judge feedback...\n")

        story = revise_story(user_request, story, judge_result)

        # Show the revised story for this iteration
        print("\n----- REVISED STORY (iteration {}) -----\n".format(iteration))
        print(story)
        print("\n----------------------------------------\n")

        # Re-judge the new version
        judge_result = judge_story(user_request, story)
        print("----- UPDATED JUDGE RESULT -----")
        print(judge_result)

    print("\n=== FINAL STORY AFTER AUTOMATED LOOP ===\n")
    print(story)

    print("\n=== FINAL JUDGE SUMMARY AFTER AUTOMATED LOOP ===")
    overall = judge_result.get("overall_score")
    print(f"Overall score: {overall}/10")
    print("Detailed scores:", {k: v for k, v in judge_result.items() if k != "improvements"})
    print("\nSuggested improvements (if any):")
    for tip in judge_result.get("improvements", []):
        print(f"- {tip}")

    # 4) NEW: Let the user request manual changes
    print("\n----------------------------------------")
    print("Would you like to request any changes to the story?")
    print("For example: 'make it shorter', 'more funny', 'more engaging'.")
    user_feedback = input("Enter feedback or press Enter to keep the story as is: ").strip()

    if user_feedback:
        print("\n[EXTRA] Revising story based on your feedback (and still respecting safety)...\n")
        story = revise_story(user_request, story, judge_result, user_feedback=user_feedback)

        # Optionally re-judge the feedback-based version
        judge_result = judge_story(user_request, story)

        print("\n=== UPDATED STORY AFTER USER FEEDBACK ===\n")
        print(story)

        print("\n=== UPDATED JUDGE SUMMARY AFTER USER FEEDBACK ===")
        overall = judge_result.get("overall_score")
        print(f"Overall score: {overall}/10")
        print("Detailed scores:", {k: v for k, v in judge_result.items() if k != "improvements"})
        print("\nSuggested improvements (if any):")
        for tip in judge_result.get("improvements", []):
            print(f"- {tip}")
    else:
        print("\nNo additional feedback provided. Story kept as-is.")


if __name__ == "__main__":
    run_story_loop()
