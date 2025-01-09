import bs4
from langchain_community.document_loaders import WebBaseLoader


page_url = "https://habr.com/ru/companies/sherpa_rpa/articles/847058/"
loader = WebBaseLoader(
    web_paths=[page_url],
    bs_kwargs={
        "parse_only": bs4.SoupStrainer(attrs={"id": "post-content-body"})
    }
)
web_pages = loader.load()
print(len(web_pages))
print(web_pages[0].metadata, web_pages[0].page_content)
