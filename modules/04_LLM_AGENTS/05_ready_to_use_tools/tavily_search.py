import os
from langchain_community.tools import TavilySearchResults


os.environ["TAVILY_API_KEY"] = "..."
tool = TavilySearchResults(
    max_results=10,
    search_depth="advanced",
    include_answer=False,
    include_raw_content=True,
    include_images=False,
    # include_domains=[...],
    # exclude_domains=[...],
)

result = tool.invoke({"query": "The best course for development MVP AI service"})
print(result)
