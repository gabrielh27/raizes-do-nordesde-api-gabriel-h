from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.seguranca import gerar_hash_senha

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("", response_model=schemas.UsuarioResposta, status_code=201)
def cadastrar_usuario(dados: schemas.UsuarioCriar, db: Session = Depends(get_db)):
    existe = db.query(models.Usuario).filter(models.Usuario.email == dados.email).first()
    if existe:
        raise HTTPException(status_code=409, detail="E-mail ja cadastrado.")

    novo = models.Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash_senha(dados.senha),
        perfil=dados.perfil,
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)

    if dados.consentimento_lgpd:
        fidelidade = models.Fidelidade(usuario_id=novo.id, consentimento_lgpd=True)
        db.add(fidelidade)
        db.commit()

    return novo