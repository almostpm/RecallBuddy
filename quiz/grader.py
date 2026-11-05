from educhain.prompts.prompt import PromptTemplate
from educhain.output_parsers.parser import StringOutputParser
from educhain.core.sequence import RunnableSequence
from config import get_chat_model, GROQ_MODELS
from quiz.models import QuizQuestion


def grade_answer(quiz_q: QuizQuestion, user_choice_index: int) -> str:
    if not isinstance(quiz_q, QuizQuestion):
        raise TypeError("quiz_q must be a QuizQuestion")
    if not isinstance(user_choice_index, int) or not (0 <= user_choice_index <= 3):
        raise ValueError("user_choice_index must be an integer between 0 and 3")

    is_correct = (user_choice_index == quiz_q.correct_index)

    last_error = None
    for model_name in GROQ_MODELS:
        try:
            model = get_chat_model(model_name=model_name)

            template = """The user was asked: {question}
The correct answer is: {correct_answer}
The user answered: {user_answer}
Here is the context from the source material: {context}
The user got the question {result}.
Please provide a short, encouraging, plain-language explanation of WHY the correct answer is right, and if they were wrong, gently explain where their thinking might have gone off track. Keep it under 3 sentences."""

            input_variables = ["question", "correct_answer", "user_answer", "context", "result"]

            chain: RunnableSequence[dict, str] = PromptTemplate(template=template, input_variables=input_variables) | model | StringOutputParser()

            question_val = quiz_q.question
            correct_answer_val = quiz_q.options[quiz_q.correct_index]
            user_answer_val = quiz_q.options[user_choice_index]
            context_val = quiz_q.source_chunk
            result_val = "Right" if is_correct else "Wrong"

            inputs = {
                "question": question_val,
                "correct_answer": correct_answer_val,
                "user_answer": user_answer_val,
                "context": context_val,
                "result": result_val
            }

            response = chain.invoke(inputs)
            return response
        except Exception as e:
            last_error = e
            print(f"DEBUG ERROR grade_answer with model {model_name}: {str(e)}")
            continue

    raise RuntimeError(f"All Groq models failed. Last error: {last_error}")