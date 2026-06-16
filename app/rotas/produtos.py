from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.dependencias import exigir_perfil

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("", response_model=schemas.ProdutoResposta, status_code=201)
def criar_produto(
    dados: schemas.ProdutoCriar,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_perfil("ADMIN", "GERENTE")),
):
    novo = models.Produto(nome=dados.nome, descricao=dados.descricao, preco=dados.preco)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("", response_model=list[schemas.ProdutoResposta])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(models.Produto).all()


@router.get("/{produto_id}", response_model=schemas.ProdutoResposta)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto nao encontrado.")
    return produto