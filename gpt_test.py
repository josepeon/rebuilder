import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

def query_together(prompt):
    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        },
    )
    return response.json()["choices"][0]["message"]["content"]

if __name__ == "__main__":
    prompt = "Explain what Python decorators are in plain English."
    print("\nRebuilder Response:\n")
    print(query_together(prompt))