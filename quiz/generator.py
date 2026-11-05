"""Generate a multiple-choice quiz question from retrieved context."""

from educhain.prompts.prompt import PromptTemplate
from educhain.output_parsers.parser import JsonOutputParser
from educhain.core.rag import RAGChain

from config import get_chat_model, GROQ_MODELS
from quiz.models import QuizQuestion


def generate_question(vectorstore, topic: str) -> QuizQuestion:
    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("topic must be a non-empty string")

    last_error = None
    for model_name in GROQ_MODELS:
        try:
            model = get_chat_model(model_name=model_name)

            prompt = PromptTemplate(
                template="""Based on the following context, generate exactly ONE multiple-choice question about {question}.
Context: {context}
Return ONLY a valid JSON object with these keys:
- "question": string
- "options": list of exactly 4 strings
- "correct_index": integer (0 to 3)
- "explanation": string (why the correct answer is right)
- "source_chunk": string (the context chunk the question was derived from)
Do not include any markdown formatting or extra text.""",
                input_variables=["context", "question"],
            )

            parser = JsonOutputParser()
            chain = prompt | model | parser
            rag_chain = RAGChain(vectorstore, chain)
            result = rag_chain.invoke(topic)

            return QuizQuestion(
                question=result["question"],
                options=result["options"],
                correct_index=result["correct_index"],
                explanation=result["explanation"],
                source_chunk=result["source_chunk"],
            )
        except Exception as e:
            last_error = e
            print(f"DEBUG ERROR generate_question with model {model_name}: {str(e)}")
            continue

    raise RuntimeError(f"All Groq models failed. Last error: {last_error}")