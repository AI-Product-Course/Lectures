import json
import requests


OLLAMA_HOST = "localhost"
OLLAMA_PORT = "11434"
GET_MODELS_ENDPOINT = "api/tags"

URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/{GET_MODELS_ENDPOINT}"

response = requests.get(URL)
data = response.json()
print(json.dumps(data, indent=4))
