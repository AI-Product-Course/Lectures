from pydantic import BaseModel, Field
from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL


class ToolInput(BaseModel):
    code: str = Field(description="Python code to execute.")


python_repl = PythonREPL()
repl_tool = Tool(
    name="python_repl",
    description="Executes python code and returns the result. The code runs in a static sandbox without interactive mode, so print output or save output to a file.",
    func=python_repl.run,
)
repl_tool.args_schema = ToolInput

result = repl_tool.invoke("print(1+1)")
print(result)
