from typing import Optional
import chainlit as cl


users = [
    cl.User(identifier="1", display_name="Admin", metadata={"username": "admin", "password": "admin"}),
    cl.User(identifier="2", display_name="Nick", metadata={"username": "nick", "password": "super"}),
    cl.User(identifier="3", display_name="Dan", metadata={"username": "dan", "password": "ultra"}),
]


@cl.password_auth_callback
def on_login(username: str, password: str) -> Optional[cl.User]:
    for user in users:
        current_username, current_password = user.metadata["username"], user.metadata["password"]
        if current_username == username and current_password == password:
            return user
    return None


@cl.on_chat_start
async def on_chat_start():
    current_user = cl.user_session.get("user")
    await cl.Message(f"Добро пожаловать, {current_user.display_name}").send()
