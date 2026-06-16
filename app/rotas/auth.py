from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.seguranca import verificar_senha, criar_token

router = APIRouter(prefix="/auth", tags=["Autenticacao"])


@router.post("/login", response_model=schemas.TokenResposta)
def login(dados: schemas.LoginEntrada, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == dados.email
    ).first()

    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha invalidos.")

    token = criar_token({"sub": str(usuario.id), "perfil": usuario.perfil})
    return schemas.TokenResposta(access_token=token, perfil=usuario.perfil)


@router.post("/token", response_model=schemas.TokenResposta)
def login_swagger(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == form.username
    ).first()

    if not usuario or not verificar_senha(form.password, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha invalidos.")

    token = criar_token({"sub": str(usuario.id), "perfil": usuario.perfil})
    return schemas.TokenResposta(access_token=token, perfil=usuario.perfil)