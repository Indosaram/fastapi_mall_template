from pydantic import BaseModel


class Item(BaseModel):
    id: str | None = None
    title: str
    price: int
    thumbnail: str | None = None
    category: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "6182a806347ed04e12d4b2a2",
                "title": "iPhone 13 Pro Max",
                "price": 1300000,
                "category": "mobile",
            }
        }
