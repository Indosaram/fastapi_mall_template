from passlib.context import CryptContext


class Hasher:
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, password: str):
        return cls.pwd_ctx.hash(password)

    @classmethod
    def verify(cls, hashed_password: str, plain_password: str):
        return cls.pwd_ctx.verify(plain_password, hashed_password)
