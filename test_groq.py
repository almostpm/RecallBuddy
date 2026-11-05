from config import get_chat_model
import os
from dotenv import load_dotenv
load_dotenv()

print("Key exists:", bool(os.environ.get("GROQ_API_KEY")))
try:
    model = get_chat_model()
    response = model.invoke("Say hello in one word")
    print("SUCCESS:", response.content)
except Exception as e:
    print("EXACT ERROR:", repr(e))