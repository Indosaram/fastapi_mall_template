from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from auth.token import create_access_token
from database import client
from utils.hasher import Hasher

db = client.mall_template
router = APIRouter(tags=["auth"])


@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends()):
    collection = db["user"]
    user = await collection.find_one({"name": request.username})

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{request.name}' is not found.",
        )

    if not Hasher.verify(user["password"], request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect password",
        )
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
