import uvicorn
from fastapi import FastAPI
from app.routes.login import router as LoginRouter
from app.routes.user import router as UserRouter

app = FastAPI(
    title="Sistema de Control de Accesos",
    description="Aplicación FastAPI con JWT",
    version="1.0.0",
)

app.include_router(LoginRouter, tags=["Autenticación"], prefix="/login")
app.include_router(UserRouter, tags=["Usuarios"], prefix="/user")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=5003, reload=True)
