import chainlit as cl


@cl.on_chat_start
async def main():
    ask = cl.AskUserMessage(content="Напиши свое имя", timeout=10)
    result = await ask.send()
    if result:
        name = result["output"]
        cl.user_session.set("name", name)
        msg = cl.Message(content=f"Привет, {name}! Напиши свой вопрос")
        await msg.send()
    else:
        await ask.remove()


@cl.on_message
async def send():
    name = cl.user_session.get("name", default="незнакомец")
    msg = cl.Message(content=f"Спасибо за вопрос, {name}")
    await msg.send()
