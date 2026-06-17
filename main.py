from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.rotas import usuarios, auth, unidades, produtos
from app.rotas import usuarios, auth, unidades, produtos, estoque
from app.rotas import usuarios, auth, unidades, produtos, estoque, pedidos
from app.rotas import usuarios, auth, unidades, produtos, estoque, pedidos, pagamentos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Raizes do Nordeste")

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(unidades.router)
app.include_router(produtos.router)
app.include_router(estoque.router)
app.include_router(pedidos.router)
app.include_router(pagamentos.router)


@app.get("/")
def raiz():
    return {"mensagem": "API Raizes do Nordeste no ar"}