# API Back-end — Rede "Raízes do Nordeste"

API REST desenvolvida como Projeto Multidisciplinar (Trilha Back-end) do curso de Análise e Desenvolvimento de Sistemas — UNINTER.

A solução atende a uma rede de lanchonetes nordestinas em expansão, com pedidos por múltiplos canais (App, Totem, Balcão, Pick-up e Web), controle de estoque por unidade, programa de fidelização com consentimento LGPD e integração simulada (mock) de pagamento.

---

## Tecnologias utilizadas

- **Python 3.13**
- **FastAPI** — framework da API REST
- **Uvicorn** — servidor ASGI
- **SQLAlchemy** — ORM (mapeamento objeto-relacional)
- **SQLite** — banco de dados (arquivo local, sem instalação)
- **bcrypt** — hash de senhas
- **python-jose** — geração e validação de tokens JWT
- **Pydantic** — validação de dados (schemas)

---

## Requisitos

- Python 3.11 ou superior instalado
- Git (para clonar o repositório)

---

## Como executar (passo a passo)

### 1. Clonar o repositório

```bash
git clone https://github.com/gabrielh27/raizes-do-nordesde-api-gabriel-h.git
cd raizes-do-nordesde-api-gabriel-h
```

### 2. Criar e ativar o ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Popular o banco com dados iniciais (seed)

```bash
python seed.py
```

Esse comando cria o banco `raizes.db` e popula com usuários, unidades, produtos e estoque de teste.

### 5. Iniciar a API

```bash
uvicorn main:app --reload
```

A API ficará disponível em: **http://127.0.0.1:8000**

---

## Documentação da API (Swagger / OpenAPI)

Com a API rodando, acesse a documentação interativa em:

**http://127.0.0.1:8000/docs**

Pelo Swagger é possível visualizar todos os endpoints, testar requisições e autenticar-se (botão **Authorize**).

---

## Autenticação

A API usa autenticação **JWT** com três perfis de acesso (roles):

- **CLIENTE** — realiza e consulta pedidos, consulta cardápio e fidelidade
- **GERENTE** — gerencia produtos, unidades e estoque
- **ADMIN** — acesso administrativo completo

### Usuários criados pelo seed

| Perfil   | E-mail               | Senha       |
|----------|----------------------|-------------|
| ADMIN    | admin@teste.com      | admin123    |
| CLIENTE  | maria@teste.com      | senha123    |
| GERENTE  | gerente@teste.com    | gerente123  |

Para autenticar no Swagger: clique em **Authorize**, informe o e-mail no campo *username* e a senha no campo *password*.

---

## Principais endpoints

| Recurso       | Método | Rota                              | Auth        |
|---------------|--------|-----------------------------------|-------------|
| Autenticação  | POST   | `/auth/login`                     | Público     |
| Usuários      | POST   | `/usuarios`                       | Público     |
| Unidades      | GET    | `/unidades`                       | Público     |
| Unidades      | POST   | `/unidades`                       | ADMIN/GERENTE |
| Produtos      | GET    | `/produtos`                       | Público     |
| Produtos      | POST   | `/produtos`                       | ADMIN/GERENTE |
| Estoque       | POST   | `/estoque`                        | ADMIN/GERENTE |
| Estoque       | GET    | `/estoque/unidade/{id}`           | Público     |
| Pedidos       | POST   | `/pedidos`                        | Autenticado |
| Pedidos       | GET    | `/pedidos?canal_pedido=APP`       | Autenticado |
| Pedidos       | PATCH  | `/pedidos/{id}/status`            | Autenticado |
| Pagamentos    | POST   | `/pagamentos`                     | Autenticado |
| Fidelidade    | GET    | `/fidelidade/meu-saldo`           | Autenticado |

---

## Fluxo crítico (Pedido → Pagamento → Status)

1. Cliente cria um pedido (`POST /pedidos`) informando a unidade, o canal (`canal_pedido`) e os itens. A API valida estoque, calcula o total e cria o pedido com status `AGUARDANDO_PAGAMENTO`, baixando o estoque.
2. O pagamento é solicitado (`POST /pagamentos`). O serviço externo é simulado (mock): se aprovado, o pedido passa a `PAGO`; se recusado, passa a `CANCELADO`.
3. O status do pedido pode ser atualizado pela operação (`PATCH /pedidos/{id}/status`): `EM_PREPARO` → `PRONTO` → `ENTREGUE`.

---

## Plano de testes

A coleção de testes do Postman está no arquivo:

```
Raizes_do_Nordeste.postman_collection.json
```

Para executar: importe o arquivo no Postman, garanta que a API está rodando e que o seed foi executado, e use **Run collection**. São 14 cenários (positivos e negativos), cobrindo autenticação, autorização (401/403), validações, regra de estoque (409) e pagamento mock.

---

## Segurança e LGPD

- Senhas armazenadas com **hash bcrypt** (nunca em texto puro)
- Autenticação por **token JWT** com expiração
- Autorização por **perfil/role** aplicada nos endpoints
- Dados sensíveis **não são expostos** nas respostas (a senha nunca retorna)
- Programa de fidelidade exige **consentimento explícito** do cliente (LGPD)

---

## Estrutura do projeto

```
.
├── app/
│   ├── rotas/
│   │   ├── auth.py
│   │   ├── usuarios.py
│   │   ├── unidades.py
│   │   ├── produtos.py
│   │   ├── estoque.py
│   │   ├── pedidos.py
│   │   ├── pagamentos.py
│   │   └── fidelidade.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── seguranca.py
│   └── dependencias.py
├── main.py
├── seed.py
├── requirements.txt
├── Raizes_do_Nordeste.postman_collection.json
└── README.md
```
