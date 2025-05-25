from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mistralai import ChatMistralAI


DEFAULT_SESSION_ID = "default"
chat_history = InMemoryChatMessageHistory()


messages = [
    ("system", "You are an expert in {domain}. Your task is answer the question as short as possible"),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
]
prompt = ChatPromptTemplate(messages)

trimmer = trim_messages(
    strategy="last",
    token_counter=len,
    max_tokens=10,
    start_on="human",
    end_on="human",
    include_system=True,
    allow_partial=False
)

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    mistral_api_key="..."
)


chain = prompt | trimmer | llm
chain_with_history = RunnableWithMessageHistory(
    chain, lambda session_id: chat_history,
    input_messages_key="question", history_messages_key="history"
)
final_chain = chain_with_history | StrOutputParser()


domain = input('Choice domain area: ')
while True:
    print()
    user_question = input('You: ')
    print('Bot: ', end="")
    for answer_chunk in final_chain.stream(
            {"domain": domain, "question": user_question},
            config={"configurable": {"session_id": DEFAULT_SESSION_ID}},
    ):
        print(answer_chunk, end="")
    print()
