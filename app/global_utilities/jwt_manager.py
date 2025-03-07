import os
from jwt import encode, decode, PyJWTError
from dotenv import load_dotenv
from fastapi import Request, HTTPException, Cookie
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta, timezone
import hashlib

load_dotenv()

ACCESS_TOKEN_SECRET = os.getenv(
    "ACCESS_TOKEN_SECRET", "access-token-secret-dev-environment"
)
REFRESH_TOKEN_SECRET = os.getenv(
    "REFRESH_TOKEN_SECRET", "refresh-token-secret-dev-environment"
)


def generate_random_string() -> str:
    return os.urandom(40).hex()


ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(data: dict, fingerprint: str) -> str:
    fingerprint_hash = hashlib.sha256(fingerprint.encode()).hexdigest()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = data.copy()
    payload.update({"fingerprint": fingerprint_hash, "exp": expire})
    access_token: str = encode(
        payload=payload, key=ACCESS_TOKEN_SECRET, algorithm="HS256"
    )
    return access_token


def create_refresh_token(data: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = data.copy()
    payload.update({"exp": expire})
    refresh_token: str = encode(
        payload=payload, key=REFRESH_TOKEN_SECRET, algorithm="HS256"
    )
    return refresh_token


def validate_access_token(token: str, fingerprint: str = Cookie(None)) -> dict:
    try:
        data: dict = decode(token, key=ACCESS_TOKEN_SECRET, algorithms=["HS256"])
        fingerprint_hashed_in_token = data.get("fingerprint")
        user_email = data.get("email")
        if fingerprint_hashed_in_token is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        if fingerprint is None:
            raise HTTPException(
                status_code=401, detail="Fingerprint no encontrado en la cookie"
            )
        cookie_fingerprint_hash = hashlib.sha256(fingerprint.encode()).hexdigest()
        if cookie_fingerprint_hash != fingerprint_hashed_in_token:
            raise HTTPException(status_code=401, detail="Token fingerprint mismatch")
        return {"user_email": user_email}
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


def validate_refresh_token(token: str) -> dict:
    try:
        data: dict = decode(token, key=REFRESH_TOKEN_SECRET, algorithms=["HS256"])
        return data
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Refresh token inválido o expirado")


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        try:
            payload = validate_access_token(
                auth.credentials, fingerprint=request.cookies.get("fingerprint")
            )
            email = payload.get("user_email")
            if email is None:
                raise HTTPException(status_code=403, detail="Token inválido o expirado")
        except PyJWTError:
            raise HTTPException(status_code=403, detail="Credenciales inválidas")
        return email
