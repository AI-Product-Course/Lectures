from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage


llm = ChatOllama(
    model="llama3.2",
    temperature=0,
    num_predict=150
)

messages_1 = [
    SystemMessage(content="You translate Russian to English. Translate the user sentence and write only result:"),
    HumanMessage(content="Я создам успешный AI-продукт!")
]
messages_2 = [
    SystemMessage(content="You translate Russian to English. Translate the user sentence and write only result:"),
    HumanMessage(content="У меня ничего не получится!")
]


# Standard
ai_message = llm.invoke(messages_1)
print(ai_message.content)

# Stream
for message_chunk in llm.stream(messages_1):
    print(message_chunk.content, end="")
print()

# Batch
ai_message_1, ai_message_2 = llm.batch([messages_1, messages_2])
print(ai_message_1.content)
print(ai_message_2.content)
