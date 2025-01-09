from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_mistralai import ChatMistralAI

llm = ChatMistralAI(
    model="open-mistral-7b",
    temperature=0,
    mistral_api_key="..."
)


class Person(BaseModel):
    firstname: str = Field(description="fullname of hero")
    lastname: str = Field(description="fullname of hero")
    age: int = Field(description="age of hero")


parser = PydanticOutputParser(pydantic_object=Person)

messages = [
    ("system", "Handle the user query.\n{format_instructions}"),
    ("human", "{user_query}")
]
prompt_template = ChatPromptTemplate(messages)
prompt_value = prompt_template.invoke(
    {
        "format_instructions": parser.get_format_instructions(),
        "user_query": "Генрих Смит был восемнацдцателетним юношей, мечтающим уехать в город"
    }
)

answer = llm.invoke(prompt_value.to_messages())
print(parser.invoke(answer))
