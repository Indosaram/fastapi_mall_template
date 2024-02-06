from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends


from auth.oauth2 import get_current_user
from auth.schemas import TokenData
from database import get_conn
from item.schemas import Item

router = APIRouter(prefix="/item", tags=["item"])


@router.get("/")
async def all_items(
    limit: int = 100,
    category: str | None = None,
    conn: get_conn = Depends(),
) -> dict[str, list[Item]]:
    items = conn.execute("SELECT * FROM items;")

    return {"data": items}


@router.get("/{id}")
async def item(id: str) -> Item:
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
)
async def create(
    request: Item, current_user: TokenData = Depends(get_current_user)
) -> Item:
    collection = db["items"]
    new_article = await collection.insert_one(jsonable_encoder(request))
    created_article = await collection.find_one({"_id": new_article.inserted_id})

    created_article["id"] = str(created_article["_id"])

    return created_article


@router.delete("/{id}")
async def destroy(id: str, current_user: TokenData = Depends(get_current_user)):
    collection = db["items"]
    delete_result = await collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No item is found by provided id: {id}",
        )

    return delete_result


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update(id: str, request: dict) -> Item:
    collection = db["items"]
    item = await collection.find_one({"_id": ObjectId(id)})

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No item is found by provided id: {id}",
        )

    updated = await collection.find_one_and_update(
        {"_id": item["_id"]}, {"$set": request}, return_document=ReturnDocument.AFTER
    )
    updated["id"] = str(updated["_id"])

    return updated
