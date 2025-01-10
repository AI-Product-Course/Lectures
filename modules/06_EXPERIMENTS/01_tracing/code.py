from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnableConfig
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openinference.instrumentation.langchain import LangChainInstrumentor
from phoenix.otel import register


# trace registration
tracer_provider = register(
  project_name="mvp-ai-course",
  endpoint="http://localhost:6006/v1/traces",
)
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

# data ingestion and preparation
loader = PyPDFLoader("./paper.pdf")
pages = loader.load()[:10]
full_text = "\n".join(page.page_content for page in pages)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600, chunk_overlap=200, add_start_index=True
)
text_chunks = text_splitter.split_text(full_text)
documents = [Document(page_content=text, metadata={"source": "paper.pdf"}) for text in text_chunks]

# vector store and retriever
embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")
vectorstore = InMemoryVectorStore.from_documents(
    documents,
    embedding=embeddings,
)
retriever = vectorstore.as_retriever(k=5)

# LLM
llm = ChatMistralAI(
    model="open-mistral-7b",
    temperature=0,
    mistral_api_key="..."
)

# prompt
prompt = ChatPromptTemplate.from_messages([
    (
      "system", (
        "You are an assistant for QA. Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, just say that you don't know. Answer as short as possible. "
        "Context: {context}"
      )
    ),
    ("human", "Question: {question}")
])

# format documents for context
format_docs_runnable = (
  RunnableLambda(lambda docs: "\n\n".join(d.page_content for d in docs))
  .with_config(config=RunnableConfig(run_name="format documents"))
)

# final chain
chain = RunnableParallel(
    context=retriever | format_docs_runnable,
    question=lambda data: data
) | prompt | llm | StrOutputParser()
result = chain.invoke("What is attention?")
print(result)
