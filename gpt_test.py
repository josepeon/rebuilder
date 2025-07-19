from openai import OpenAI
from dotenv import load_dotenv
import os

# Load the .env file to access the API key
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def test_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    prompt = "Explain briefly what Python decorators do."
    explanation = test_gpt(prompt)
    print("\nGPT Response:\n")
    print(explanation)

    # Change API next
    