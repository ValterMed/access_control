from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum


Role = Enum(
    value="Role",
    names=[
        ("Normal", 1648),
        ("Administrator", 2591),
    ],
)


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john_doe@email.com",
                "password": "secret",
            }
        }


class UserSchema(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    role: Role = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "jhon@email.com",
                "password": "password",
                "role": 1648,
            }
        }
