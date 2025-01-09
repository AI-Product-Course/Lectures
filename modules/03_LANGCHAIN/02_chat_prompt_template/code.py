from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage


messages = [
    ("system", "You are helpful assistant. Current date: {current_date} and time: {current_time}"),
    MessagesPlaceholder("history"),
]
prompt_template = ChatPromptTemplate(messages)

current_datetime = datetime.now()
prompt_value = prompt_template.invoke(
    {
        "history": [HumanMessage(content='Какое сейчас время?')],
        "current_date": current_datetime.date(),
        "current_time": current_datetime.time(),
    }
)
print(prompt_value.to_messages())
