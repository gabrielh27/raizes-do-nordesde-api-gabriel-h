from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.rotas import usuarios, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Raizes do Nordeste")

app.include_router(auth.router)
app.include_router(usuarios.router)


@app.get("/")
def raiz():
    return {"mensagem": "API Raizes do Nordeste no ar"}