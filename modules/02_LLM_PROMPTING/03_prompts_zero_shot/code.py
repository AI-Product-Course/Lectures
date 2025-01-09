from openai import OpenAI


API_KEY = "..."
BASE_URL = "https://api.mistral.ai/v1"
MODEL_NAME = "mistral-small-latest"


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

system_message = """\
Classify the text into neutral, negative or positive
Text:
"""

user_message = "I think the vacation is okay."

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
