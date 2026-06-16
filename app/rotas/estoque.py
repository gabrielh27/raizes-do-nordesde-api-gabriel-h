from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.dependencias import exigir_perfil

router = APIRouter(prefix="/estoque", tags=["Estoque"])


@router.post("", response_model=schemas.EstoqueResposta, status_code=201)
def movimentar_estoque(
    dados: schemas.EstoqueEntrada,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_perfil("ADMIN", "GERENTE")),
):
    unidade = db.query(models.Unidade).filter(models.Unidade.id == dados.unidade_id).first()
    if unidade is None:
        raise HTTPException(status_code=404, detail="Unidade nao encontrada.")

    produto = db.query(models.Produto).filter(models.Produto.id == dados.produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto nao encontrado.")

    estoque = db.query(models.Estoque).filter(
        models.Estoque.unidade_id == dados.unidade_id,
        models.Estoque.produto_id == dados.produto_id,
    ).first()

    if estoque is None:
        estoque = models.Estoque(
            unidade_id=dados.unidade_id,
            produto_id=dados.produto_id,
            quantidade=dados.quantidade,
        )
        db.add(estoque)
    else:
        estoque.quantidade += dados.quantidade

    db.commit()
    db.refresh(estoque)
    return estoque


@router.get("/unidade/{unidade_id}", response_model=list[schemas.EstoqueResposta])
def consultar_estoque(unidade_id: int, db: Session = Depends(get_db)):
    return db.query(models.Estoque).filter(models.Estoque.unidade_id == unidade_id).all()