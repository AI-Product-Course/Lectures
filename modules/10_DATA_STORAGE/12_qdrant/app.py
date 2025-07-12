import qdrant_client
from typing import Annotated

from fastapi import FastAPI, Body, Depends
from pydantic import BaseModel, Field
from langchain_huggingface.embeddings import HuggingFaceEmbeddings


COLLECTION_NAME = "spams"
THRESHOLD = 0.5


async def get_qdrant_client():
    yield qdrant_client.AsyncQdrantClient(url="http://localhost:6333")


QdrantClient = Annotated[qdrant_client.AsyncQdrantClient, Depends(get_qdrant_client)]


embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")
app = FastAPI()


class Document(BaseModel):
    id: str
    is_spam: bool
    text: str

class QueryRequest(BaseModel):
    query: str = Field(examples=["Win a VIP weekend getaway! Text HOLIDAY to 63355 for your chance to claim (£2/msg)"])
    k: int = Field(examples=[5])

class QueryResponse(BaseModel):
    best_documents: list[Document]
    is_spam: bool
    probability: float



@app.post("/predict", response_model=QueryResponse)
async def predict_spam_fact(client: QdrantClient, data: QueryRequest = Body()) -> QueryResponse:
    vector = embeddings.embed_query(data.query)
    result = await client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=data.k,
        with_payload=True,
        with_vectors=False,
    )
    documents = [
        Document(id=point.id, is_spam=point.payload["is_spam"], text=point.payload["text"])
        for point in result.points
    ]
    probability = sum([doc.is_spam for doc in documents]) / len(documents)

    return QueryResponse(
        best_documents=documents,
        is_spam=probability > THRESHOLD,
        probability=probability
    )
