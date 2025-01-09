from openai import OpenAI


API_KEY = "..."
BASE_URL = "https://api.mistral.ai/v1"
MODEL_NAME = "mistral-small-latest"


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

system_message = """\
Solve the task by following the examples below.
Examples:
1) Task: The odd numbers in this group add up to an even number: 4, 8, 9, 15, 12, 2, 1.
Assistant: Adding all the odd numbers (9, 15, 1) gives 25. The answer is False.
2) Task: The odd numbers in this group add up to an even number: 16,  11, 14, 4, 8, 13, 24.
Assistant: Adding all the odd numbers (11, 13) gives 24. The answer is True.
"""

user_message = "Task: The odd numbers in this group add up to an even number: 17,  10, 19, 4, 8, 12, 24. Assistant: "

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": system_message,
        },
        {
            "role": "user",
            "content": user_message,
        }
    ],
    model=MODEL_NAME,
    temperature=0.1
)

print(chat_completion.choices[0].message.content)
