from openai import OpenAI


API_KEY = "..."
BASE_URL = "https://api.mistral.ai/v1"
MODEL_NAME = "mistral-small-latest"


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

message = """\
Solve the task. Think step by step and give answer in format "Answer is True or False"
Task: Check if the odd numbers in this group add up to an even number: 17,  10, 19, 4, 8, 12, 24
"""

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": message,
        },
    ],
    model=MODEL_NAME,
    temperature=0.1
)


print(chat_completion.choices[0].message.content)
