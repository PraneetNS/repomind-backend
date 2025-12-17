import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

def generate_answer(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )
    return response.json()["response"]
