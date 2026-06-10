from datetime import datetime, timedelta
import bcrypt
from jose import jwt, JWTError

CHAVE_SECRETA = "troque-esta-chave-por-uma-bem-secreta-12345"
ALGORITMO = "HS256"
EXPIRA_MINUTOS = 60


def gerar_hash_senha(senha: str) -> str:
    senha_bytes = senha.encode("utf-8")
    hash_bytes = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    return hash_bytes.decode("utf-8")


def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    senha_bytes = senha_pura.encode("utf-8")
    hash_bytes = senha_hash.encode("utf-8")
    return bcrypt.checkpw(senha_bytes, hash_bytes)


def criar_token(dados: dict) -> str:
    para_codificar = dados.copy()
    expira = datetime.utcnow() + timedelta(minutes=EXPIRA_MINUTOS)
    para_codificar.update({"exp": expira})
    return jwt.encode(para_codificar, CHAVE_SECRETA, algorithm=ALGORITMO)


def decodificar_token(token: str):
    try:
        payload = jwt.decode(token, CHAVE_SECRETA, algorithms=[ALGORITMO])
        return payload
    except JWTError:
        return None