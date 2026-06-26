import os
from dotenv import load_dotenv

load_dotenv()

try:
    from groq import Groq
except ModuleNotFoundError:  
    Groq = None

client = None
if Groq is not None:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def call_groq(prompt: str):
    if client is None:
        raise RuntimeError("Groq client is not available. Install the 'groq' package and set GROQ_API_KEY.")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


def generate(prompt: str):
    return call_groq(prompt)