# pip install langchain_huggingface

import numpy as np
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document


def similarity_score(vector1: np.array, vector2: np.array) -> float:
    return (
        np.sum(vector1 * vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    )


relevant_doc = Document(page_content="passage: Большая языковая модель это языковая модель, состоящая из нейронной сети со множеством параметров (обычно миллиарды весовых коэффициентов и более), обученной на большом количестве неразмеченного текста с использованием обучения без учителя.")
irrelevant_doc = Document(page_content="passage: Задачи сокращения размерности. Исходная информация представляется в виде признаковых описаний, причём число признаков может быть достаточно большим. Задача состоит в том, чтобы представить эти данные в пространстве меньшей размерности, по возможности, минимизировав потери информации..")


embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")

document_vectors = embeddings.embed_documents([relevant_doc.page_content, irrelevant_doc.page_content])
query_vector = embeddings.embed_query("query: Что такое большая языковая модель?")

print("Relevant document score:", similarity_score(np.array(query_vector), np.array(document_vectors[0])))
print("Irrelevant document score:", similarity_score(np.array(query_vector), np.array(document_vectors[1])))
