import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# ------------------ NORMAL CHAT ------------------
def get_response(query, history=None):
    try:
        if history is None:
            history = []

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


# ------------------ RAG CHAT ------------------
def rag_response(query, text):
    try:
        context = text[:2000]

        messages = [
            {"role": "system", "content": "Answer based only on the given document."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]

        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",
            messages=messages
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"ERROR: {str(e)}"