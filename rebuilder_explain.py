import requests
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

ALLOWED_EXTENSIONS = [".py", ".js", ".json", ".md", ".txt"]
MAX_CHUNKS = 10

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

def explain_chunk(chunk, mode, retries=2):
    if mode == "2":
        prompt = f"Suggest improvements, refactors, or rewrite strategies for the following code:\n\n{chunk}"
    else:
        prompt = f"Explain the following code or configuration in detail:\n\n{chunk}"

    for attempt in range(retries + 1):
        try:
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
        except Exception as e:
            if attempt < retries:
                print(f"Retrying ({attempt+1}/{retries}) due to error: {e}")
                time.sleep(2)
            else:
                return f"Error after retries: {e}"

def format_as_markdown(chunks, explanations):
    md = "# Rebuilder Output\n\n"
    for i, (chunk, explanation) in enumerate(zip(chunks, explanations), 1):
        md += f"## Chunk {i}\n\n"
        md += "```text\n" + chunk + "\n```\n\n"
        md += f"**Explanation:**\n\n{explanation.strip()}\n\n"
    return md

def is_supported_file(path):
    return any(path.endswith(ext) for ext in ALLOWED_EXTENSIONS)

if __name__ == "__main__":
    mode = input("Choose mode: (1) Explain or (2) Rebuild Suggestion: ").strip()
    path = input("Enter path to file to explain: ").strip()
    
    if not is_supported_file(path):
        print("Unsupported file type.")
        exit()
    
    content = load_file(path)
    chunks = chunk_text(content)
    
    if len(chunks) > MAX_CHUNKS:
        print(f"Warning: File is long. Only processing first {MAX_CHUNKS} chunks.")
        chunks = chunks[:MAX_CHUNKS]
    
    explanations = []
    for i, chunk in enumerate(chunks):
        print(f"\n--- Original Chunk {i+1} ---\n")
        print(chunk)
        
        print(f"\n--- Explanation {i+1} ---\n")
        explanation = explain_chunk(chunk, mode)
        print(explanation)
        explanations.append(explanation)

    save = input("Do you want to save this as a markdown file? (y/n): ").strip().lower()
    if save == "y":
        md_output = format_as_markdown(chunks, explanations)
        with open("rebuilder_output.md", "w", encoding="utf-8") as f:
            f.write(md_output)
        print("Saved as rebuilder_output.md")