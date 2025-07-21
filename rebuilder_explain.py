import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

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

def format_as_markdown(chunks, explanations):
    md = "# Rebuilder Output\n\n"
    for i, (chunk, explanation) in enumerate(zip(chunks, explanations), 1):
        md += f"## Chunk {i}\n\n"
        md += "```text\n" + chunk + "\n```\n\n"
        md += f"**Explanation:**\n\n{explanation.strip()}\n\n"
    return md

if __name__ == "__main__":
    path = input("Enter path to file to explain: ").strip()
    content = load_file(path)
    chunks = chunk_text(content)
    
    explanations = []
    for i, chunk in enumerate(chunks):
        print(f"\n--- Original Chunk {i+1} ---\n")
        print(chunk)
        
        print(f"\n--- Explanation {i+1} ---\n")
        explanation = explain_chunk(chunk)
        print(explanation)
        explanations.append(explanation)

    save = input("Do you want to save this as a markdown file? (y/n): ").strip().lower()
    if save == "y":
        md_output = format_as_markdown(chunks, explanations)
        with open("rebuilder_output.md", "w", encoding="utf-8") as f:
            f.write(md_output)
        print("Saved as rebuilder_output.md")