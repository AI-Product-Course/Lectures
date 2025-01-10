from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_mistralai import ChatMistralAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.docstore.document import Document
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import chainlit as cl


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        (
            "You are an assistant for QA. Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, just say that you don't know. Answer as short as possible. "
            "Context: {context} \n Question:"
        )
    ),
    ("human", "{question}")
])

llm = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0,
    mistral_api_key="..."
)

embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")


@cl.on_chat_start
async def on_chat_start():
    files = None

    while not files:
        ask_file = cl.AskFileMessage(
            content="Пожалуйста загрузите pdf-файл",
            accept=["application/pdf"],
            max_size_mb=20,
            timeout=180,
        )
        files = await ask_file.send()
        if not files:
            await ask_file.remove()

    file = files[0]

    msg = cl.Message(content=f"Обрабатывается файл {file.name}...")
    await msg.send()

    loader = PyPDFLoader(file.path)
    chunks = loader.load_and_split(
        RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)
    )

    msg.content = f"Файл {file.name} разбит на {len(chunks)} чанков"
    await msg.update()

    vectorstore = InMemoryVectorStore.from_documents(chunks, embeddings)

    msg.content = f"Векторное хранилище построено на основе чанков из файла {file.name}"
    await msg.update()

    retriever = vectorstore.as_retriever()
    chain = RunnableParallel(
        context=retriever, question=lambda question: question
    ) | RunnableParallel(answer=prompt | llm | StrOutputParser(), chunks=lambda data: data["context"])
    cl.user_session.set("chain", chain)

    await cl.sleep(2)
    msg.content = f"Можете задавать вопросы по файлу {file.name}"
    await msg.update()


@cl.on_message
async def main(message: cl.Message):
    chain: Runnable = cl.user_session.get("chain")

    res = await chain.ainvoke(message.content)
    answer: str = res["answer"]
    chunks: List[Document] = res["chunks"]

    text_elements = [
        cl.Text(content=chunk.page_content, name=f"Фрагмент для контекста", display="inline")
        for index, chunk in enumerate(chunks)
    ]
    await cl.Message(content=answer, elements=text_elements).send()
