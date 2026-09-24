import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    messages=[
        {
            "role": "user",
            "content": "Jelaskan apa itu python dalam satu kalimat.",
        }
    ],
)

print(response.choices[0].message.content)
# if api_key:
#     print("API key berhasil terbaca")
# else:
#     print("API key tidak terbaca")
