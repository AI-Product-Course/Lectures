FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py app.py

EXPOSE 8000

CMD ["fastapi", "dev", "--host", "0.0.0.0", "app.py"]