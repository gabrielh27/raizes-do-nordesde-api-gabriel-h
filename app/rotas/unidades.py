from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.dependencias import usuario_logado, exigir_perfil

router = APIRouter(prefix="/unidades", tags=["Unidades"])


@router.post("", response_model=schemas.UnidadeResposta, status_code=201)
def criar_unidade(
    dados: schemas.UnidadeCriar,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_perfil("ADMIN", "GERENTE")),
):
    nova = models.Unidade(nome=dados.nome, cidade=dados.cidade)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@router.get("", response_model=list[schemas.UnidadeResposta])
def listar_unidades(db: Session = Depends(get_db)):
    return db.query(models.Unidade).all()


@router.get("/{unidade_id}", response_model=schemas.UnidadeResposta)
def buscar_unidade(unidade_id: int, db: Session = Depends(get_db)):
    unidade = db.query(models.Unidade).filter(models.Unidade.id == unidade_id).first()
    if unidade is None:
        raise HTTPException(status_code=404, detail="Unidade nao encontrada.")
    return unidade