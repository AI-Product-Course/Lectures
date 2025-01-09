from openai import OpenAI


API_KEY = "ollama"
BASE_URL = "http://localhost:11434/v1/"
MODEL_NAME = "llama3.2"


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

message = "Привет! Когда ждать появления AGI?"

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": message,
        }
    ],
    model=MODEL_NAME,
    temperature=0.1
)

print(chat_completion.choices[0].message.content)
