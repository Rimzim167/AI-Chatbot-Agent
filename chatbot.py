from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def get_response(query, history=[]):
    try:
        messages = []

        for h in history:
            messages.append({"role": "user", "content": h[0]})
            messages.append({"role": "assistant", "content": h[1]})

        messages.append({"role": "user", "content": query})

        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",
            messages=messages
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"ERROR: {str(e)}"
    
def rag_response(query, text):
    context = text[:2000]

    messages = [
        {"role": "system", "content": "Answer based on given document."},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
    ]

    response = client.chat.completions.create(
        model="meta-llama/llama-3-8b-instruct",
        messages=messages
    )

    return response.choices[0].message.content