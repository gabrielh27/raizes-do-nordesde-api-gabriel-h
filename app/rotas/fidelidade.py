from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.dependencias import usuario_logado

router = APIRouter(prefix="/fidelidade", tags=["Fidelidade"])


@router.get("/meu-saldo", response_model=schemas.FidelidadeResposta)
def meu_saldo(
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(usuario_logado),
):
    fidelidade = db.query(models.Fidelidade).filter(
        models.Fidelidade.usuario_id == usuario.id
    ).first()

    if fidelidade is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente sem programa de fidelidade (consentimento LGPD nao registrado).",
        )

    return fidelidade