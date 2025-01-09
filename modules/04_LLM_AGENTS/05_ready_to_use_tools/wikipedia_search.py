from langchain.agents import Tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang="en"))
wikipedia_tool = Tool(
    name="wikipedia",
    description="Search in Wikipedia knowledge database.",
    func=wikipedia.run,
)
result = wikipedia_tool.invoke("Large Language Models")
print(result)
