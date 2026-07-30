import ollama
import re
import json


def calculate_average(question):

    numbers = re.findall(r'\d+(?:\.\d+)?', question)

    print("Extracted numbers:", numbers)

    if len(numbers) > 0:
        numbers = [float(x) for x in numbers]

        avg = sum(numbers) / len(numbers)

        return {
            "average": avg
        }

    return None


def solve_question(question):

    if "average" in question.lower():

        result = calculate_average(question)

        if result:
            return json.dumps(result)


    prompt = f"""
You are a professional data analyst.

Solve this question carefully.

Rules:
- Return ONLY valid JSON.
- No explanation.
- No markdown.

Question:
{question}
"""


    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response["message"]["content"]