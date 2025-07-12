import uuid

from qdrant_client import models, QdrantClient
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import pandas as pd


COLLECTION_NAME = "spams"
DATASET_PATH = "spams.csv"


df = pd.read_csv(DATASET_PATH) # Category,Message
print("Датасет загружен")


embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")
texts = df["Message"].to_list()
spam_facts = df["Category"].map(lambda cat: cat == "spam").to_list()
vectors = embeddings.embed_documents(texts)
print("Вектора получены")


client = QdrantClient(url="http://localhost:6333")
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
)
print("Создана коллекция")

client.upsert(
    collection_name=COLLECTION_NAME,
    points=[
        models.PointStruct(
            id=str(uuid.uuid4()),
            payload={
                "text": text,
                "is_spam": spam_fact
            },
            vector=vector,
        )
        for text, spam_fact, vector in zip(texts, spam_facts, vectors)
    ]
)
print("Добавлены точки")