import aiosmtplib
from fastapi import FastAPI, BackgroundTasks, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()


class User(BaseModel):
    email: str
    name: str


async def send_welcome_email(email: str, name: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "parrot@gmail.com"
    smtp_password = "..."

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = email
    msg['Subject'] = "Welcome to Our Course!"

    body = f"Hello {name},\n\nThank you for registering with us!"
    msg.attach(MIMEText(body, 'plain'))

    await aiosmtplib.send(
        msg, start_tls=True,
        hostname=smtp_server, port=smtp_port,
        username=smtp_user, password=smtp_password
    )


@app.post("/register")
async def register_user(background_tasks: BackgroundTasks, user_data: User = Body()):
    # logic to save user in database
    background_tasks.add_task(send_welcome_email, user_data.email, user_data.name)
    return JSONResponse({"message": "User  registered successfully! A welcome email will be sent."})
