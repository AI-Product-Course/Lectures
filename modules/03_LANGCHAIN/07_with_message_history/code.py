import time

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, trim_messages


DEFAULT_SESSION_ID = "default"
chat_history = InMemoryChatMessageHistory()


llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    mistral_api_key="..."
)

trimmer = trim_messages(
    strategy="last",
    token_counter=len,
    max_tokens=6,
    start_on="human",
    end_on="human",
    include_system=True,
    allow_partial=False
)

chain = trimmer | llm
chain_with_history = RunnableWithMessageHistory(chain, lambda session_id: chat_history)

chain_with_history.invoke(
    [HumanMessage("Hi, my name is Bob!")],
    config={"configurable": {"session_id": DEFAULT_SESSION_ID}},
)
time.sleep(2)
ai_message = chain_with_history.invoke(
    [HumanMessage("What is my name?")],
    config={"configurable": {"session_id": DEFAULT_SESSION_ID}},
)
print(ai_message.content)
