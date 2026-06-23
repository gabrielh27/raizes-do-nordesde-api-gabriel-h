from app.database import SessionLocal, Base, engine
from app import models
from app.seguranca import gerar_hash_senha

Base.metadata.create_all(bind=engine)

db = SessionLocal()


def criar_usuario(nome, email, senha, perfil, consentimento):
    existe = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if existe:
        return existe
    usuario = models.Usuario(
        nome=nome,
        email=email,
        senha_hash=gerar_hash_senha(senha),
        perfil=perfil,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    if consentimento:
        fid = models.Fidelidade(usuario_id=usuario.id, consentimento_lgpd=True)
        db.add(fid)
        db.commit()
    return usuario


def criar_unidade(nome, cidade):
    existe = db.query(models.Unidade).filter(models.Unidade.nome == nome).first()
    if existe:
        return existe
    unidade = models.Unidade(nome=nome, cidade=cidade)
    db.add(unidade)
    db.commit()
    db.refresh(unidade)
    return unidade


def criar_produto(nome, descricao, preco):
    existe = db.query(models.Produto).filter(models.Produto.nome == nome).first()
    if existe:
        return existe
    produto = models.Produto(nome=nome, descricao=descricao, preco=preco)
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


def criar_estoque(unidade_id, produto_id, quantidade):
    existe = db.query(models.Estoque).filter(
        models.Estoque.unidade_id == unidade_id,
        models.Estoque.produto_id == produto_id,
    ).first()
    if existe:
        return existe
    estoque = models.Estoque(
        unidade_id=unidade_id, produto_id=produto_id, quantidade=quantidade
    )
    db.add(estoque)
    db.commit()
    db.refresh(estoque)
    return estoque


print("Criando dados iniciais...")

criar_usuario("Gabriel Admin", "admin@teste.com", "admin123", "ADMIN", True)
criar_usuario("Maria Cliente", "maria@teste.com", "senha123", "CLIENTE", True)
criar_usuario("Joao Gerente", "gerente@teste.com", "gerente123", "GERENTE", True)

u1 = criar_unidade("Raizes Recife Centro", "Recife")
u2 = criar_unidade("Raizes Caruaru", "Caruaru")

p1 = criar_produto("Cuscuz com Carne de Sol", "Cuscuz nordestino com carne de sol", 18.90)
p2 = criar_produto("Tapioca de Queijo Coalho", "Tapioca recheada com queijo coalho", 12.50)
p3 = criar_produto("Suco de Caja", "Suco natural de caja 400ml", 8.00)

criar_estoque(u1.id, p1.id, 100)
criar_estoque(u1.id, p2.id, 100)
criar_estoque(u1.id, p3.id, 100)
criar_estoque(u2.id, p1.id, 50)
criar_estoque(u2.id, p2.id, 50)

db.close()
print("Dados iniciais criados com sucesso!")