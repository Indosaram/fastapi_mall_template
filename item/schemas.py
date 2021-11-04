from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    id: Optional[str]
    title: str
    price: int
    thumbnail: Optional[str]
    category: str

    class Config:
        schema_extra = {
            "example": {
                "id": "6182a806347ed04e12d4b2a2",
                "title": "iPhone 13 Pro Max",
                "price": 1300000,
                "category": "mobile",
            }
        }
