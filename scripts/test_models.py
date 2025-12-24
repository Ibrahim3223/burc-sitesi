# Test Groq models
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

models_to_test = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]

for model in models_to_test:
    try:
        result = client.chat.completions.create(
            messages=[{"role": "user", "content": "Merhaba"}],
            model=model,
            max_tokens=10
        )
        print(f"[OK] {model} - Calisiyor!")
        break
    except Exception as e:
        print(f"[HATA] {model} - {str(e)[:80]}")
