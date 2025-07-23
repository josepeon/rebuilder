
# Import required libraries
import requests  # For making HTTP requests to the API
import os        # For environment variable and file path handling
from dotenv import load_dotenv  # For loading environment variables from .env file
import time      # For sleep/retry logic


# Load environment variables from .env file and get API key
load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")


# Supported file extensions and max number of code chunks to process
ALLOWED_EXTENSIONS = [".py", ".js", ".json", ".md", ".txt"]
MAX_CHUNKS = 10


# Read the entire contents of a file as a string
def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


# Split text into chunks of up to max_lines lines each
def chunk_text(text, max_lines=30):
    lines = text.splitlines()
    chunks = []
    for i in range(0, len(lines), max_lines):
        chunk = '\n'.join(lines[i:i+max_lines])
        chunks.append(chunk)
    return chunks


# Send a chunk of code to the Together API for explanation or suggestions
# Retries up to 'retries' times if an error occurs
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


# Format the code chunks and their explanations as a Markdown document
def format_as_markdown(chunks, explanations):
    md = "# Rebuilder Output\n\n"
    for i, (chunk, explanation) in enumerate(zip(chunks, explanations), 1):
        md += f"## Chunk {i}\n\n"
        md += "```text\n" + chunk + "\n```\n\n"
        md += f"**Explanation:**\n\n{explanation.strip()}\n\n"
    return md


# Check if the file extension is supported
def is_supported_file(path):
    return any(path.endswith(ext) for ext in ALLOWED_EXTENSIONS)


# Main script logic: user interaction and workflow
if __name__ == "__main__":
    # Prompt user for mode and file path
    mode = input("Choose mode: (1) Explain or (2) Rebuild Suggestion: ").strip()
    path = input("Enter path to file to explain: ").strip()
    
    # Check if file type is supported
    if not is_supported_file(path):
        print("Unsupported file type.")
        exit()
    
    # Load file and split into chunks
    content = load_file(path)
    chunks = chunk_text(content)
    
    # Warn and limit if file is too long
    if len(chunks) > MAX_CHUNKS:
        print(f"Warning: File is long. Only processing first {MAX_CHUNKS} chunks.")
        chunks = chunks[:MAX_CHUNKS]
    
    explanations = []
    # Process each chunk: print and explain
    for i, chunk in enumerate(chunks):
        print(f"\n--- Original Chunk {i+1} ---\n")
        print(chunk)
        
        print(f"\n--- Explanation {i+1} ---\n")
        explanation = explain_chunk(chunk, mode)
        print(explanation)
        explanations.append(explanation)

    # Optionally save output as markdown
    save = input("Do you want to save this as a markdown file? (y/n): ").strip().lower()
    if save == "y":
        md_output = format_as_markdown(chunks, explanations)
        with open("rebuilder_output.md", "w", encoding="utf-8") as f:
            f.write(md_output)
        print("Saved as rebuilder_output.md")