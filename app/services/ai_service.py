import os
from dotenv import load_dotenv
from groq import Groq
from fastapi import HTTPException

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


def ask_ai(prompt):
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


def create_prompt(context, question):
    return f"""
        Gunakan catatan berikut sebagai konteks menjawab pertanyaan.
        
        Catatan:
        "{context}"
        
        Pertanyaan:
        "{question}"
    """


def ask_note(context, question):
    prompt = create_prompt(context, question)
    return prompt


def create_summary_prompt(context):
    return f"""
    Ringkas catatan berikut secara singkat dan jelas
    
    Catatan:
    "{context}"
    """
