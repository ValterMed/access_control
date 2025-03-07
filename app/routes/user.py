import os
from app.global_utilities.jwt_manager import JWTBearer
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

environment = os.getenv("ENVIRONMENT", "develop")

from app.database import get_users
from app.database import add_user
from app.models.user import UserSchema

router = APIRouter()


@router.get(
    "/",
    response_description="Users data retrieved successfully",
    dependencies=[Depends(JWTBearer())],
)
async def get_users_data():
    users = get_users()
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(users),
    )


@router.post(
    "/",
    response_description="User data added into the database",
    dependencies=[Depends(JWTBearer())],
)
async def add_user_data(user: UserSchema):
    user = jsonable_encoder(user)
    new_user = add_user(user)
    if new_user:
        return JSONResponse(
            status_code=200,
            content={"message": "User added successfully", "data": new_user},
        )
    return JSONResponse(
        status_code=409,
        content={"message": "User already registered"},
    )
