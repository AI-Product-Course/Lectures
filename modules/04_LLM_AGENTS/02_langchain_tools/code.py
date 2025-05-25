import time
from langchain_core.tools import tool
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage
from pydantic import Field


ORDERS_STATUSES_DATA = {
    "a42": "Доставляется",
    "b61": "Выполнен",
    "k37": "Отменен",
}


@tool
def get_order_status(order_id: str = Field(description="Identifier of order")) -> str:
    """Get status of order by order identifier"""
    return ORDERS_STATUSES_DATA.get(order_id, f"Не существует заказа с order_id={order_id}")


llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    mistral_api_key="..."
)
llm_with_tools = llm.bind_tools([get_order_status])

messages = [
    HumanMessage(content="What about my order k37?")
]
ai_message = llm_with_tools.invoke(messages)
messages.append(ai_message)

for tool_call in ai_message.tool_calls:
    if tool_call["name"] == get_order_status.name:
        tool_message = get_order_status.invoke(tool_call)
        messages.append(tool_message)

time.sleep(2)
ai_message = llm_with_tools.invoke(messages)
messages.append(ai_message)
print(ai_message.content)
