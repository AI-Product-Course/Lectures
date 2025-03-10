from uuid import uuid4, UUID
from pydantic import BaseModel, Field


class BaseBook(BaseModel):
    name: str = Field(examples=["Война и Мир"])
    author: str = Field(examples=["Л. Н. Толстой"])
    year: int = Field(examples=[1868])
    annotation: str = Field(examples=["Классический роман-эпопея рассказывает о сложном, бурном периоде в истории России и всей Европы с 1805 по 1812 год. "])


class Book(BaseBook):
    id: UUID = Field(examples=[uuid4()])


class CreateBook(BaseBook):
    ...

class UpdateBook(BaseBook):
    ...

class SuccessMessage(BaseModel):
    message: str = Field(examples=["Операция успешно выполнена"])
