from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "indo",
                "email": "freedomzero91@gmail.com",
                "password": "projex",
            }
        }


class UserList(BaseModel):
    data: List[User]
