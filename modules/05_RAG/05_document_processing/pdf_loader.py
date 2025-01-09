from langchain_community.document_loaders import PyPDFLoader


loader = PyPDFLoader("./paper.pdf")
pages = loader.load()
print(len(pages))
print(pages[0].page_content[:100])
print(pages[0].metadata)
