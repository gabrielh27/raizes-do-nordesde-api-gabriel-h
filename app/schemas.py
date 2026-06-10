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