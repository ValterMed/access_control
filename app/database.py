import os
from argon2.exceptions import VerifyMismatchError
from app.global_utilities.jwt_manager import (
    create_access_token,
    create_refresh_token,
)
from app.global_utilities.hashing import get_password_hasher

# las passwords "sin hash para probar" son password1, password2, password3, password4, password5
FAKE_DB = {
    "email1@email.com": {
        "email": "email1@email.com",
        "password": "$argon2d$v=19$m=19456,t=2,p=1$goGDKbcUSsQ3CxealvcKZQ$KzU4YbQ8p7Z1RIpa9mwqNw",
    },
    "email2@email.com": {
        "email": "email2@email.com",
        "password": "$argon2d$v=19$m=19456,t=2,p=1$NC5++ydyDHpwwYj91JPvpQ$yMWPaI0/gVSTjRP+9N+0bg",
    },
    "email3@email.com": {
        "email": "email3@email.com",
        "password": "$argon2d$v=19$m=19456,t=2,p=1$PBOzpnXWpbebHGU8iFLfDA$rhgR6sUcSn6rN/x5g6WtOQ",
    },
    "email4@email.com": {
        "email": "email4@email.com",
        "password": "$argon2d$v=19$m=19456,t=2,p=1$r5IIcazqYmexWYZ/vaUtXA$SHvD6UDbZ4rYja9ouT5mEg",
    },
    "email5@email.com": {
        "email": "email5@email.com",
        "password": "$argon2d$v=19$m=19456,t=2,p=1$onqI+0yxfgF7oB44MkQbOA$nMM3bEreKai4XhKSMdrEmQ",
    },
}


def generate_random_string() -> str:
    return os.urandom(40).hex()


def search_user_in_fake_db(email: str) -> dict:
    return FAKE_DB.get(email, None)


def login_user(user: dict) -> dict:
    current_user = search_user_in_fake_db(user["email"])
    if current_user:
        password_hasher = get_password_hasher()
        user_password = user["password"]
        hashed_password = current_user["password"]

        try:
            password_hasher.verify(hashed_password, user_password)
            data = {
                "email": current_user["email"],
            }

            fingerprint = os.urandom(40).hex()
            access_token = create_access_token(data, fingerprint)
            refresh_token = create_refresh_token({"email": user["email"]})

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "fingerprint": fingerprint,
            }
        except VerifyMismatchError:
            return {"error": "Credenciales inválidas"}
    else:
        return {"error": "usuario/contraseña incorrectas"}


def add_user(user: dict) -> dict:
    if user["email"] in FAKE_DB:
        return f"Usuario con email {user['email']} ya existe"

    password = user.get("password")
    ph = get_password_hasher()
    hashed_password = ph.hash(password)
    user["password"] = hashed_password

    # TODO Guardar en base de datos real
    return {**user, "message": "Usuario creado con éxito"}


def get_users():
    return FAKE_DB
