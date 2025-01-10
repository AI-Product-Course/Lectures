import chainlit as cl


@cl.on_message
async def flip_message(message: cl.Message):
    raw_text = message.content
    raw_answer = raw_text[::-1]
    message = cl.Message(content=raw_answer)
    await message.send()
