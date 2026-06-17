from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.dependencias import usuario_logado

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

CANAIS_VALIDOS = ["APP", "TOTEM", "BALCAO", "PICKUP", "WEB"]


@router.post("", response_model=schemas.PedidoResposta, status_code=201)
def criar_pedido(
    dados: schemas.PedidoCriar,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(usuario_logado),
):
    if dados.canal_pedido not in CANAIS_VALIDOS:
        raise HTTPException(
            status_code=422,
            detail=f"canal_pedido invalido. Use um de: {CANAIS_VALIDOS}",
        )

    unidade = db.query(models.Unidade).filter(models.Unidade.id == dados.unidade_id).first()
    if unidade is None:
        raise HTTPException(status_code=404, detail="Unidade nao encontrada.")

    if not dados.itens:
        raise HTTPException(status_code=422, detail="O pedido deve ter ao menos um item.")

    total = 0.0
    itens_validados = []

    for item in dados.itens:
        produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id).first()
        if produto is None:
            raise HTTPException(status_code=404, detail=f"Produto {item.produto_id} nao encontrado.")

        estoque = db.query(models.Estoque).filter(
            models.Estoque.unidade_id == dados.unidade_id,
            models.Estoque.produto_id == item.produto_id,
        ).first()

        if estoque is None or estoque.quantidade < item.quantidade:
            disponivel = estoque.quantidade if estoque else 0
            raise HTTPException(
                status_code=409,
                detail=f"Estoque insuficiente para o produto {produto.nome}. Disponivel: {disponivel}.",
            )

        total += produto.preco * item.quantidade
        itens_validados.append((produto, item.quantidade, estoque))

    pedido = models.Pedido(
        usuario_id=usuario.id,
        unidade_id=dados.unidade_id,
        canal_pedido=dados.canal_pedido,
        status="AGUARDANDO_PAGAMENTO",
        total=total,
    )
    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    for produto, quantidade, estoque in itens_validados:
        item_pedido = models.ItemPedido(
            pedido_id=pedido.id,
            produto_id=produto.id,
            quantidade=quantidade,
            preco_unitario=produto.preco,
        )
        db.add(item_pedido)
        estoque.quantidade -= quantidade

    db.commit()
    db.refresh(pedido)
    return pedido


@router.get("", response_model=list[schemas.PedidoResposta])
def listar_pedidos(
    canal_pedido: str | None = None,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(usuario_logado),
):
    query = db.query(models.Pedido)
    if canal_pedido:
        query = query.filter(models.Pedido.canal_pedido == canal_pedido)
    return query.all()


@router.get("/{pedido_id}", response_model=schemas.PedidoResposta)
def buscar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(usuario_logado),
):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido nao encontrado.")
    return pedido