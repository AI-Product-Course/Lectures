import json
import time

from mistralai import Mistral


API_KEY = "..."
MODEL_NAME = "mistral-large-latest"


ORDERS_STATUSES_DATA = {
    "a42": "Доставляется",
    "b61": "Выполнен",
    "k37": "Отменен",
}


def get_order_status(order_id: str) -> str:
    return ORDERS_STATUSES_DATA.get(order_id, f"Не существует заказа с order_id={order_id}")


def cancel_order(order_id: str) -> str:
    if order_id not in ORDERS_STATUSES_DATA:
        return f"Не существует заказа с order_id={order_id}"
    if ORDERS_STATUSES_DATA[order_id] != "Отменен":
        ORDERS_STATUSES_DATA[order_id] = "Отменен"
        return "Заказ успешно отменен"
    return "Заказ уже отменен"


NAMES_TO_FUNCTIONS = {
    "get_order_status": get_order_status,
    "cancel_order": cancel_order
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Get status of order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order identifier",
                    }
                },
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_order",
            "description": "Cancel the order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order identifier",
                    }
                },
                "required": ["order_id"],
            },
        },
    },
]


client = Mistral(api_key=API_KEY)
messages = [
    {
        "role": "user",
        "content": "Отмени заказ a42"
    },
]
print("User:", messages[0]["content"])

chat_response = client.chat.complete(
    model=MODEL_NAME,
    messages=messages,
    tools=TOOLS,
    tool_choice="auto",
)
messages.append(chat_response.choices[0].message)
print("Function Calling:", chat_response.choices[0].message.tool_calls[0])

tool_call = chat_response.choices[0].message.tool_calls[0]
function_name = tool_call.function.name
function_params = json.loads(tool_call.function.arguments)
function_result = NAMES_TO_FUNCTIONS[function_name](**function_params)
messages.append({"role": "tool", "name": function_name, "content": function_result, "tool_call_id": tool_call.id})
print("function_name: ", function_name)
print("function_params: ", function_params)
print("function_result: ", function_result)

time.sleep(2)

chat_response = client.chat.complete(
    model=MODEL_NAME,
    messages=messages,
)
print("Final answer:", chat_response.choices[0].message.content)
