import json
from json import JSONDecodeError

import requests


OLLAMA_HOST = "localhost"
OLLAMA_PORT = "11434"
SEND_MESSAGE_URL = "api/generate"
URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/{SEND_MESSAGE_URL}"

MODEL_NAME = "llama3.2:3b"


prompt = input("You: ")
while prompt.lower() != "stop":
    parameters = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
    }
    with requests.post(url=URL, json=parameters, stream=True) as response:
        response.raise_for_status()
        print("AI assistant: ", end="")
        for chunk_content in response.iter_content(chunk_size=1024):
            try:
                chunk_data = json.loads(chunk_content)
                print(chunk_data["response"], end="")
            except JSONDecodeError as ex:
                pass # в конце приходят некорректные символы, которые можно пропустить
        print("")
    prompt = input("You: ")
