from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "indo",
                "email": "freedomzero91@gmail.com",
                "password": "projex",
            }
        }
