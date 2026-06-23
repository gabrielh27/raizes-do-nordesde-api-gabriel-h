from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.dependencias import usuario_logado

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


@router.post("", response_model=schemas.PagamentoResposta, status_code=201)
def processar_pagamento(
    dados: schemas.PagamentoEntrada,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(usuario_logado),
):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == dados.pedido_id).first()
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido nao encontrado.")

    if pedido.status != "AGUARDANDO_PAGAMENTO":
        raise HTTPException(
            status_code=409,
            detail=f"Pedido nao esta aguardando pagamento (status atual: {pedido.status}).",
        )

    if dados.aprovar:
        status_pagamento = "APROVADO"
        retorno = "Pagamento aprovado pelo gateway externo (mock)."
        pedido.status = "PAGO"

        fidelidade = db.query(models.Fidelidade).filter(
            models.Fidelidade.usuario_id == pedido.usuario_id
        ).first()
        if fidelidade is not None:
            fidelidade.pontos += int(pedido.total // 10)
    else:
        status_pagamento = "RECUSADO"
        retorno = "Pagamento recusado pelo gateway externo (mock)."
        pedido.status = "CANCELADO"

    pagamento = models.Pagamento(
        pedido_id=pedido.id,
        status=status_pagamento,
        valor=pedido.total,
        retorno_mock=retorno,
    )
    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)
    return pagamento