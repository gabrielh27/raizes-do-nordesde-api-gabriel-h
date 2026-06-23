from pydantic import BaseModel, EmailStr
from datetime import datetime


class UsuarioCriar(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    perfil: str = "CLIENTE"
    consentimento_lgpd: bool = False


class UsuarioResposta(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: str
    criado_em: datetime

    class Config:
        from_attributes = True


class LoginEntrada(BaseModel):
    email: EmailStr
    senha: str


class TokenResposta(BaseModel):
    access_token: str
    token_type: str = "bearer"
    perfil: str



class UnidadeCriar(BaseModel):
    nome: str
    cidade: str


class UnidadeResposta(BaseModel):
    id: int
    nome: str
    cidade: str
    ativa: bool

    class Config:
        from_attributes = True

class ProdutoCriar(BaseModel):
    nome: str
    descricao: str | None = None
    preco: float


class ProdutoResposta(BaseModel):
    id: int
    nome: str
    descricao: str | None = None
    preco: float

    class Config:
        from_attributes = True

class EstoqueEntrada(BaseModel):
    unidade_id: int
    produto_id: int
    quantidade: int


class EstoqueResposta(BaseModel):
    id: int
    unidade_id: int
    produto_id: int
    quantidade: int

    class Config:
        from_attributes = True

class ItemPedidoEntrada(BaseModel):
    produto_id: int
    quantidade: int


class PedidoCriar(BaseModel):
    unidade_id: int
    canal_pedido: str
    itens: list[ItemPedidoEntrada]


class ItemPedidoResposta(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: float

    class Config:
        from_attributes = True


class PedidoResposta(BaseModel):
    id: int
    usuario_id: int
    unidade_id: int
    canal_pedido: str
    status: str
    total: float
    itens: list[ItemPedidoResposta]

    class Config:
        from_attributes = True

class PagamentoEntrada(BaseModel):
    pedido_id: int
    aprovar: bool = True


class PagamentoResposta(BaseModel):
    id: int
    pedido_id: int
    status: str
    valor: float
    retorno_mock: str | None = None

    class Config:
        from_attributes = True
    
class StatusEntrada(BaseModel):
     status: str

class FidelidadeResposta(BaseModel):
    usuario_id: int
    pontos: int
    consentimento_lgpd: bool

    class Config:
        from_attributes = True