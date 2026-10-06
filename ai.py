import json
import os

import requests

from dotenv import load_dotenv


load_dotenv()


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)


def ask_ollama(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 200,
                "temperature": 0.2
            }
        },
        timeout=180
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "response",
        ""
    ).strip()


def ask_ai(
    question,
    context
):
    """
    Answer only from uploaded notes.
    """

    if not context.strip():

        return (
            "I couldn't find this information "
            "in your uploaded notes."
        )

    prompt = f"""
You are MemoryMap AI.

You are a learning assistant that answers
ONLY from the student's uploaded study notes.

IMPORTANT RULES:

1. Use only the provided notes.
2. Do not use outside knowledge.
3. Do not guess.
4. Do not invent information.
5. If the answer is not present in the notes,
   say exactly:

I couldn't find this information in your uploaded notes.

6. Give a simple student-friendly answer.

STUDY NOTES:
-------------------------
{context}
-------------------------

QUESTION:
{question}

ANSWER:
"""

    return ask_ollama(prompt)


def generate_quiz(
    context,
    number_of_questions
):

    if not context.strip():
        return []

    prompt = f"""
You are MemoryMap AI Quiz Generator.

Create exactly {number_of_questions}
multiple-choice questions from ONLY
the provided study notes.

Rules:

- Use only the study notes.
- Do not use outside knowledge.
- Each question must have 4 options.
- Only one answer should be correct.
- Return ONLY valid JSON.
- Do not use markdown.

Format:

[
  {{
    "question": "Question",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": 0,
    "topic": "Topic"
  }}
]

Answer:
0 = A
1 = B
2 = C
3 = D

STUDY NOTES:
-------------------------
{context}
-------------------------
"""

    try:

        result = ask_ollama(
            prompt
        )

        result = result.strip()

        if result.startswith(
            "```"
        ):

            result = result.replace(
                "```json",
                ""
            )

            result = result.replace(
                "```",
                ""
            )

            result = result.strip()

        quiz = json.loads(
            result
        )

        if isinstance(
            quiz,
            list
        ):
            return quiz

        return []

    except Exception:

        return []