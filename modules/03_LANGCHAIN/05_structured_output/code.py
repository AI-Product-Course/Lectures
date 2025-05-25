from pydantic import BaseModel, Field
from langchain_mistralai import ChatMistralAI

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    mistral_api_key="..."
)


class Person(BaseModel):
    firstname: str = Field(description="fullname of hero")
    lastname: str = Field(description="fullname of hero")
    age: int = Field(description="age of hero")


messages = [
    ("system", "Handle the user query"),
    ("human", "Генрих Смит был восемнацдцателетним юношей, мечтающим уехать в город")
]


prepared_llm = llm.with_structured_output(Person)
answer = prepared_llm.invoke(messages)
print(answer)
