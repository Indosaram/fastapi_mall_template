import bson
from bson.objectid import ObjectId
from fastapi import status
from starlette.responses import Response


def validate_id(id: str, response: Response):
    try:
        object_id = ObjectId(id)
    except bson.errors.InvalidId as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": str(exc)}

    return object_id
