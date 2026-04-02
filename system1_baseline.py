import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = (
    "You are a programming tutor specializing in Data Structures, Algorithms, "
    "and Web Development. Answer questions clearly and concisely."
)


def ask_baseline(question: str) -> dict:
    start = time.time()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        max_tokens=300,
        temperature=0.3,
    )

    elapsed = round(time.time() - start, 2)
    answer = response.choices[0].message.content.strip()

    return {
        "system": "Baseline",
        "question": question,
        "answer": answer,
        "response_time": elapsed,
    }


if __name__ == "__main__":
    test_q = "What is binary search?"
    print(f"Question: {test_q}\n")
    result = ask_baseline(test_q)
    print(f"Answer:\n{result['answer']}")
    print(f"\nResponse time: {result['response_time']}s")
