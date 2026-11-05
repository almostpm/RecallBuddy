from quiz.generator import generate_question
from quiz.grader import grade_answer
from progress.tracker import ProgressTracker


class QuizSession:
    def __init__(self, vectorstore, topic: str):
        if not isinstance(topic, str) or not topic.strip():
            raise ValueError("topic must be a non-empty string")
        self.vectorstore = vectorstore
        self.topic = topic
        self.tracker = ProgressTracker()

    def start(self) -> None:
        print("\n--- Welcome to RecallBuddy ---")
        num_questions = 3

        for i in range(num_questions):
            print(f"\nQuestion {i+1} of {num_questions}:")

            try:
                quiz_q = generate_question(self.vectorstore, self.topic)
            except Exception:
                print("Failed to generate question. Ensure API keys are set.")
                break

            print(quiz_q.question)
            for idx, option in enumerate(quiz_q.options):
                print(f"  {idx + 1}. {option}")

            user_input = input("\nYour answer (1-4): ")

            if user_input not in ["1", "2", "3", "4"]:
                print("Invalid choice. Skipping.")
                continue

            user_idx = int(user_input) - 1

            explanation = grade_answer(quiz_q, user_idx)
            print(f"\n{explanation}")

            is_correct = (user_idx == quiz_q.correct_index)
            self.tracker.record_attempt(self.topic, quiz_q.question, is_correct)

        stats = self.tracker.get_stats()
        print("\n--- Quiz Complete ---")
        print(f"Total: {stats['total']}, Correct: {stats['correct']}, Accuracy: {stats['accuracy']}%")