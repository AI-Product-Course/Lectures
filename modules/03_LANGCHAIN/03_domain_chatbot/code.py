from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
    num_predict=150
)


messages = [
    ("system", "You are an expert in {domain}. Your task is answer the question as short as possible"),
    MessagesPlaceholder("history"),
]
prompt_template = ChatPromptTemplate(messages)


domain = input('Choice domain area: ')
history = []
while True:
    print()
    user_content = input('You: ')
    history.append(HumanMessage(content=user_content))
    prompt_value = prompt_template.invoke({"domain": domain, "history": history})
    full_ai_content = ""
    print('Bot: ', end="")
    for ai_message_chunk in llm.stream(prompt_value.to_messages()):
        print(ai_message_chunk.content, end="")
        full_ai_content += ai_message_chunk.content
    history.append(AIMessage(content=full_ai_content))
    print()
