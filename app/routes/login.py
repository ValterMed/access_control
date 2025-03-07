from fastapi.responses import JSONResponse
from fastapi import APIRouter, Response
from fastapi.encoders import jsonable_encoder
from app.models.user import UserLoginSchema
from app.database import login_user
import os
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()

environment = os.getenv("ENVIRONMENT", "develop")


@router.post("/", response_description="User authentication", response_model=dict)
async def login(user: UserLoginSchema, response: Response) -> dict:
    user = jsonable_encoder(user)
    auth_data = login_user(user)

    if "access_token" in auth_data:
        access_token = auth_data["access_token"]
        refresh_token = auth_data["refresh_token"]
        json_response = JSONResponse(
            status_code=200,
            content={"access_token": access_token, "refresh_token": refresh_token},
        )
        json_response.set_cookie(
            key="fingerprint",
            value=auth_data["fingerprint"],
            httponly=True if environment == "production" else False,
            samesite="strict",
            secure=True if environment == "production" else False,
        )
        return json_response

    return JSONResponse(
        status_code=401,
        content={"error": auth_data.get("error", "Error de autenticación")},
    )
