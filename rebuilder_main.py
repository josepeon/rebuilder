import os
import glob
from rebuilder_parser import load_file, chunk_text, explain_chunk
from rebuilder_explain import format_as_markdown


def collect_python_files(path):
    if os.path.isfile(path) and path.endswith(".py"):
        return [path]
    elif os.path.isdir(path):
        return glob.glob(os.path.join(path, "**", "*.py"), recursive=True)
    else:
        raise ValueError("Input must be a .py file or a directory containing .py files")


def main():
    input_path = input("Enter the path to a Python file or folder: ").strip()
    output_path = "rebuilder_output.md"

    all_chunks = []
    all_explanations = []

    files = collect_python_files(input_path)
    for file_path in files:
        print(f"\nProcessing: {file_path}\n")
        text = load_file(file_path)
        chunks = chunk_text(text)

        explanations = []
        for chunk in chunks:
            explanation = explain_chunk(chunk)
            explanations.append(explanation)

        all_chunks.extend(chunks)
        all_explanations.extend(explanations)

    markdown = format_as_markdown(all_chunks, all_explanations)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"\nExplanation output written to: {output_path}")


if __name__ == "__main__":
    main()