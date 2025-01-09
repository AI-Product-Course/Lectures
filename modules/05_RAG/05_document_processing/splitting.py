from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


loader = PyPDFLoader("./paper.pdf")
pages = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
chunks = text_splitter.split_documents(pages)
