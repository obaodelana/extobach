from pydantic import BaseModel
from enum import StrEnum


class AvailabilityEnum(StrEnum):
    available = "In stock"
    not_available = "Out of stock"


class CurrencyEnum(StrEnum):
    cad = "CAD"
    usd = "USD"


class ProductDetails(BaseModel):
    name: str
    description: str
    price: dict[str, float] | float
    image_url: str | None = None
    currency: CurrencyEnum = CurrencyEnum.cad
    brand: str
    category: str
    availability: AvailabilityEnum | None
    rating: float | None
