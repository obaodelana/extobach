from pydantic import BaseModel


class ProductNames(BaseModel):
    suggestions: list[str]
