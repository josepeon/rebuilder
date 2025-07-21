import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

def explain_chunk(chunk):
    prompt = f"Explain the following code or configuration in detail:\n\n{chunk}"
    
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

def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def chunk_text(text, max_lines=30):
    lines = text.splitlines()
    chunks = []
    for i in range(0, len(lines), max_lines):
        chunk = '\n'.join(lines[i:i+max_lines])
        chunks.append(chunk)
    return chunks

if __name__ == "__main__":
    path = input("Enter path to file to explain: ").strip()
    content = load_file(path)
    print("\n--- File Content ---\n")
    print(content)

    chunks = chunk_text(content)
    for i, chunk in enumerate(chunks):
    print(f"\n--- Original Chunk {i+1} ---\n")
    print(chunk)
    
    print(f"\n--- Explanation {i+1} ---\n")
    explanation = explain_chunk(chunk)
    print(explanation)