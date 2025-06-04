from openai import OpenAI


API_KEY = "..."
BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "meta-llama/llama-3.3-8b-instruct:free"


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

message = "Привет! Когда ждать появления AGI?"

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "Ты чокнутый профессор, который думает, что AGI сидит у него в подвале",
        },
        {
            "role": "user",
            "content": message,
        }
    ],
    model=MODEL_NAME,
    temperature=0.7
)

print(chat_completion.choices[0].message.content)
