import os
from dotenv import load_dotenv
from groq import Groq
from fastapi import HTTPException

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        raise e
