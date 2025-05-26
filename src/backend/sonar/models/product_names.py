from pydantic import BaseModel


class ProductNames(BaseModel):
    names: list[str]
