from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from starlette.responses import Response

from database import client
from user.schemas import User, UserList
from utils.hasher import Hasher
from utils.utils import validate_id

db = client.mall_template
router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
    tags=["user"],
)
async def create(request: User):
    request.password = Hasher.hash(request.password)
    collection = db["user"]
    new_user = await collection.insert_one(jsonable_encoder(request))
    created_user = await collection.find_one({"_id": new_user.inserted_id})

    created_user["id"] = str(created_user["_id"])

    return created_user


@router.get("/", response_model=UserList)
async def index(limit: int = 100) -> dict:
    collection = db["user"]
    cursor = collection.find()

    documents = []
    for user in await cursor.to_list(length=limit):
        user["id"] = str(user["_id"])
        documents.append(user)

    return {"data": documents}


@router.get("/{id}", response_model=User)
async def show(id: str, response: Response):
    object_id = validate_id(id, response)

    collection = db["user"]
    user = await collection.find_one({"_id": object_id})

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user is found by provided id: {id}",
        )
    user["id"] = str(user["_id"])
    return user


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def destroy(id: str, response: Response):
    object_id = validate_id(id, response)
    collection = db["user"]
    delete_result = await collection.delete_one({"_id": object_id})

    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user is found by provided id: {id}",
        )

    return {"msg": f"An user of id {id} is deleted."}


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update(id: str, response: Response, request: User):
    object_id = validate_id(id, response)

    collection = db["user"]
    updated_user = await collection.find_one_and_update(
        {"_id": object_id}, {"$set": jsonable_encoder(request)}
    )

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user is found by provided id: {id}",
        )

    return {"msg": f"An user of id {id} is updated."}
