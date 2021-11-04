from typing import Dict, List

from bson.objectid import ObjectId
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

from database import client
from item.schemas import Item

db = client.mall_template
router = APIRouter(prefix="/item", tags=["item"])


@router.get("/", response_model=Dict[str, List[Item]])
async def all_items(limit: int = 100) -> dict:
    collection = db["items"]
    cursor = collection.find()

    documents = []
    for item in await cursor.to_list(length=limit):
        item["id"] = str(item["_id"])
        documents.append(item)
    return {"data": documents}


@router.get("/{id}", response_model=Item)
async def item(id: str) -> dict:
    collection = db["items"]
    item = await collection.find_one({"_id": ObjectId(id)})

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No item is found by provided id: {id}",
        )
    item["id"] = str(item["_id"])
    return item


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Item,
)
async def create(request: Item) -> dict:

    collection = db["items"]
    new_article = await collection.insert_one(jsonable_encoder(request))
    created_article = await collection.find_one(
        {"_id": new_article.inserted_id}
    )

    created_article["id"] = str(created_article["_id"])

    return created_article


@router.delete("/{id}")
async def destroy(
    id: str,
):
    collection = db["items"]
    delete_result = await collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No item is found by provided id: {id}",
        )

    return {"msg": f"An item of id {id} is deleted."}


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update(id: str, request: dict):
    collection = db["items"]
    item = await collection.find_one({"_id": ObjectId(id)})

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No item is found by provided id: {id}",
        )
    item["id"] = str(item["_id"])

    item = {**item, **request}
    await collection.find_one_and_update(
        {"_id": item["_id"]}, {"$set": item}
    )

    return {"msg": f"An item of id {id} is updated."}
