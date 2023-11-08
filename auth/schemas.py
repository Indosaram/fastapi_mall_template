from pydantic import BaseModel


class Login(BaseModel):
    name: str
    password: str

    class Config:
        json_schema_extra = {"example": {"name": "indo", "password": "projex"}}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: str | None = None
