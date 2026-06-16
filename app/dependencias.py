from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.seguranca import decodificar_token

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/token")


def usuario_logado(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    payload = decodificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token invalido ou expirado.")

    usuario_id = payload.get("sub")
    usuario = db.query(models.Usuario).filter(models.Usuario.id == int(usuario_id)).first()
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuario nao encontrado.")

    return usuario


def exigir_perfil(*perfis_permitidos):
    def verificador(usuario: models.Usuario = Depends(usuario_logado)):
        if usuario.perfil not in perfis_permitidos:
            raise HTTPException(status_code=403, detail="Voce nao tem permissao para esta acao.")
        return usuario
    return verificador