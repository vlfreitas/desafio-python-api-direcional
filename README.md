# Desafio API Direcional - Sistema de Gestão de Vendas de Imóveis

API RESTful desenvolvida para gerenciar vendas e reservas de apartamentos, com sistema de autenticação JWT.

## Arquitetura

O projeto foi desenvolvido utilizando **Clean Architecture** com as seguintes camadas:

```
src/
├── domain/              # Entidades e interfaces de repositórios
├── application/         # Casos de uso e DTOs
├── infrastructure/      # Implementações concretas (DB, Auth)
└── presentation/        # Controllers e rotas da API
```

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e de alta performance
- **SQLAlchemy**: ORM para interação com banco de dados
- **Alembic**: Gerenciamento de migrações do banco de dados
- **PostgreSQL**: Banco de dados relacional
- **JWT**: Autenticação e autorização
- **Pytest**: Framework de testes
- **Docker & Docker Compose**: Containerização

## Requisitos

- Docker
- Docker Compose

## Como Rodar o Projeto

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd desafio-python-direcional
```

### 2. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env` (opcional, o docker-compose já tem valores padrão):

```bash
cp .env.example .env
```

### 3. Inicie os containers

```bash
docker-compose up --build
```

A API estará disponível em: `http://localhost:8000`

A documentação interativa (Swagger) estará em: `http://localhost:8000/docs`

### 4. Criar um usuário inicial (opcional)

Para testar a API, você pode criar um usuário diretamente pela documentação Swagger ou via curl:

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

## Estrutura do Banco de Dados

### Tabela: clientes
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária |
| nome | VARCHAR(255) | Nome do cliente |
| cpf | VARCHAR(11) | CPF único do cliente |
| email | VARCHAR(255) | Email do cliente |
| telefone | VARCHAR(20) | Telefone do cliente |
| created_at | DATETIME | Data de criação |
| updated_at | DATETIME | Data de atualização |

### Tabela: apartamentos
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária |
| numero | VARCHAR(10) | Número único do apartamento |
| bloco | VARCHAR(10) | Bloco do apartamento |
| andar | INTEGER | Andar do apartamento |
| quartos | INTEGER | Quantidade de quartos |
| area | NUMERIC(10,2) | Área em m² |
| preco | NUMERIC(15,2) | Preço do apartamento |
| status | ENUM | Status: disponivel, reservado, vendido |
| created_at | DATETIME | Data de criação |
| updated_at | DATETIME | Data de atualização |

### Tabela: vendas
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária |
| cliente_id | INTEGER | FK para clientes |
| apartamento_id | INTEGER | FK para apartamentos |
| valor_venda | NUMERIC(15,2) | Valor total da venda |
| valor_entrada | NUMERIC(15,2) | Valor da entrada |
| data_venda | DATETIME | Data da venda |
| created_at | DATETIME | Data de criação |
| updated_at | DATETIME | Data de atualização |

### Tabela: reservas
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária |
| cliente_id | INTEGER | FK para clientes |
| apartamento_id | INTEGER | FK para apartamentos |
| data_reserva | DATETIME | Data da reserva |
| data_expiracao | DATETIME | Data de expiração |
| ativa | BOOLEAN | Se a reserva está ativa |
| created_at | DATETIME | Data de criação |
| updated_at | DATETIME | Data de atualização |

### Tabela: usuarios
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária |
| username | VARCHAR(100) | Nome de usuário único |
| email | VARCHAR(255) | Email único |
| hashed_password | VARCHAR(255) | Senha criptografada |
| is_active | BOOLEAN | Se o usuário está ativo |
| created_at | DATETIME | Data de criação |
| updated_at | DATETIME | Data de atualização |

## Autenticação JWT

### 1. Registrar um usuário

```bash
POST /auth/register
Content-Type: application/json

{
  "username": "corretor01",
  "email": "corretor@direcional.com",
  "password": "senha123"
}
```

### 2. Fazer login e obter token

```bash
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=corretor01&password=senha123
```

Resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Usar o token nas requisições

Adicione o header `Authorization` em todas as requisições protegidas:

```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Exemplos de Requisições

### Criar um Cliente

```bash
POST /clientes/
Authorization: Bearer <seu-token>
Content-Type: application/json

{
  "nome": "João Silva",
  "cpf": "12345678901",
  "email": "joao@example.com",
  "telefone": "11999999999"
}
```

### Criar um Apartamento

```bash
POST /apartamentos/
Authorization: Bearer <seu-token>
Content-Type: application/json

{
  "numero": "101",
  "bloco": "A",
  "andar": 1,
  "quartos": 2,
  "area": 65.5,
  "preco": 250000.00
}
```

### Verificar Disponibilidade de um Apartamento

```bash
GET /apartamentos/1/disponibilidade
Authorization: Bearer <seu-token>
```

### Criar uma Reserva

```bash
POST /reservas/
Authorization: Bearer <seu-token>
Content-Type: application/json

{
  "cliente_id": 1,
  "apartamento_id": 1,
  "data_expiracao": "2024-12-31T23:59:59"
}
```

### Criar uma Venda

```bash
POST /vendas/
Authorization: Bearer <seu-token>
Content-Type: application/json

{
  "cliente_id": 1,
  "apartamento_id": 1,
  "valor_venda": 250000.00,
  "valor_entrada": 50000.00
}
```

### Listar Apartamentos por Status

```bash
GET /apartamentos/?status=disponivel
Authorization: Bearer <seu-token>
```

### Cancelar uma Reserva

```bash
POST /reservas/1/cancel
Authorization: Bearer <seu-token>
```

## 🧪 Executando os Testes

### Rodar todos os testes

```bash
docker-compose exec api pytest
```

### Rodar apenas testes de integração

```bash
docker-compose exec api pytest -m integration
```

### Rodar com cobertura

```bash
docker-compose exec api pytest --cov=src tests/
```

## Cenário de Uso Completo

Este exemplo demonstra o fluxo completo de uma venda no stand:

### 1. Corretor faz login
```bash
POST /auth/login
```

### 2. Corretor cadastra o cliente
```bash
POST /clientes/
{
  "nome": "Maria Silva",
  "cpf": "98765432109",
  "email": "maria@email.com",
  "telefone": "11988888888"
}
```

### 3. Corretor verifica apartamentos disponíveis
```bash
GET /apartamentos/?status=disponivel
```

### 4. Corretor verifica disponibilidade de um apartamento específico
```bash
GET /apartamentos/1/disponibilidade
```

### 5. Cliente decide comprar e corretor cria uma reserva
```bash
POST /reservas/
{
  "cliente_id": 1,
  "apartamento_id": 1,
  "data_expiracao": "2024-12-31T23:59:59"
}
```
> **Nota**: O apartamento agora tem status "reservado"

### 6. Cliente realiza o pagamento da entrada e a venda é finalizada
```bash
POST /vendas/
{
  "cliente_id": 1,
  "apartamento_id": 1,
  "valor_venda": 250000.00,
  "valor_entrada": 50000.00
}
```
> **Nota**: O apartamento agora tem status "vendido"

## Endpoints Disponíveis

### Autenticação
- `POST /auth/register` - Registrar novo usuário
- `POST /auth/login` - Fazer login e obter token JWT

### Clientes
- `POST /clientes/` - Criar cliente
- `GET /clientes/` - Listar clientes (com paginação)
- `GET /clientes/{id}` - Buscar cliente por ID
- `PUT /clientes/{id}` - Atualizar cliente
- `DELETE /clientes/{id}` - Deletar cliente

### Apartamentos
- `POST /apartamentos/` - Criar apartamento
- `GET /apartamentos/` - Listar apartamentos (com filtro por status)
- `GET /apartamentos/{id}` - Buscar apartamento por ID
- `GET /apartamentos/{id}/disponibilidade` - Verificar disponibilidade
- `PUT /apartamentos/{id}` - Atualizar apartamento
- `DELETE /apartamentos/{id}` - Deletar apartamento

### Vendas
- `POST /vendas/` - Criar venda
- `GET /vendas/` - Listar vendas (com paginação)
- `GET /vendas/{id}` - Buscar venda por ID
- `DELETE /vendas/{id}` - Deletar venda

### Reservas
- `POST /reservas/` - Criar reserva
- `GET /reservas/` - Listar reservas (com paginação)
- `GET /reservas/{id}` - Buscar reserva por ID
- `POST /reservas/{id}/cancel` - Cancelar reserva
- `DELETE /reservas/{id}` - Deletar reserva

## Desenvolvimento Local (sem Docker)

### 1. Instalar dependências

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 2. Configurar PostgreSQL local

Crie um banco de dados PostgreSQL e atualize a variável `DATABASE_URL` no arquivo `.env`.

### 3. Rodar migrações

```bash
alembic upgrade head
```

### 4. Iniciar o servidor

```bash
uvicorn src.main:app --reload
```
## Considerações e Decisões Técnicas

### Arquitetura

**Clean Architecture**
- **Independência de frameworks**: A lógica de negócio não depende de framework qualquer biblioteca específica
- **Testabilidade**: Cada camada pode ser testada isoladamente com mocks
- **Manutenibilidade**: Mudanças em uma camada não afetam as outras 
- **Escalabilidade**: Facilita adicionar novos recursos sem quebrar código existente

### Banco de Dados

**PostgreSQL**
- Confiável e comum no desenvolvimento
- Suporte nativo a transações
- Amplamente utilizado no mercado

**Decisões de modelagem:**
- **Status do apartamento como ENUM**: Garante integridade dos dados (apenas valores válidos: disponivel, reservado, vendido)
- **Timestamps automáticos**: `created_at` e `updated_at` em todas as tabelas para auditoria
- **Cascade delete**: Ao deletar cliente/apartamento, remove vendas/reservas relacionadas automaticamente
- **Índices únicos**: CPF e número do apartamento únicos previnem duplicatas

**Alembic:**
- Versionamento do schema (track de mudanças ao longo do tempo)
- Rollback de migrations em caso de problemas
- Facilita deploy em múltiplos ambientes (dev, staging, prod)
- Colaboração em equipe (migrations como código)

### Segurança

**Autenticação JWT vs Session:**
- **Stateless**: Não precisa armazenar sessões no servidor (escalabilidade)
- **Performance**: Valida token localmente sem consultar banco
- **Mobile-friendly**: Funciona bem com apps mobile
- **Microservices**: Token pode ser validado por outros serviços

**Validações com Pydantic:**
- Validação de tipos automática
- Mensagens de erro claras
- Previne SQL injection (dados validados antes do banco)
- Documentação automática no Swagger

### Regras de Negócio

**Máquina de estados do apartamento:**
```
DISPONIVEL → (criar reserva) → RESERVADO → (criar venda) → VENDIDO
           ↖ (cancelar reserva) ↙
```

**Por que essa abordagem?**
- Garante consistência: Um apartamento não pode ter múltiplas vendas
- Rastreabilidade: Histórico completo no banco (reservas + vendas)
- Flexibilidade: Permite venda direta (disponível → vendido) ou com reserva intermediária

**Validações implementadas:**
1. Cliente/apartamento devem existir antes de criar venda/reserva
2. CPF único por cliente
3. Número único por apartamento
4. Apartamento só pode ter uma venda ativa
5. Apartamento só pode ter uma reserva ativa
6. Status atualizado automaticamente

### Testes

**Por que dois tipos de teste?**

**Testes Unitários (23 testes):**
- **Rápidos**: ~100ms total
- **Isolados**: Mockam dependências (banco, repos)
- **Foco**: Lógica de negócio pura
- **Exemplo**: "Se cliente não existe, deve lançar ValueError"

**Testes de Integração (23 testes):**
- **Completos**: Testam fluxo real (API → Service → Repository → DB)
- **Confiança**: Garantem que tudo funciona junto
- **Realistas**: Usa banco SQLite de teste
- **Exemplo**: "POST /vendas/ deve criar venda e atualizar status do apartamento"

**Por que SQLite nos testes?**
- Muito mais rápido que PostgreSQL (em memória)
- Não precisa de setup externo
- 99% compatível com PostgreSQL para testes básicos
- Cada teste tem banco limpo (isolamento)

### Docker

**Docker Compose vs Docker simples:**
- Orquestra múltiplos containers (API + PostgreSQL)
- Rede interna automática (API consegue achar o DB)
- Volumes para persistência de dados
- Health checks garantem que DB está pronto antes de subir a API

### Performance e Escalabilidade

**Paginação em todos os endpoints de listagem:**
```python
def get_all(skip: int = 0, limit: int = 100)
```
- Evita carregar milhares de registros de uma vez
- Melhora tempo de resposta
- Reduz uso de memória

**Índices no banco:**
- CPF, email, número do apartamento (campos únicos)
- Foreign keys automáticas
- Acelera queries de busca

**Conexão pool do SQLAlchemy:**
- Reusa conexões (não abre/fecha para cada request)
- Configura timeout e tamanho do pool
- Evita esgotar conexões do banco

### Decisões que NÃO tomei (e por quê)

**Cache (Redis)**: Complexidade desnecessária para o desafio

**Auditoria completa**: Apenas created_at/updated_at, auditoria completa seria muito esforço

### Melhorias Futuras possiveis

1. **Observabilidade**: Logs estruturados, métricas, tracing
2. **Notificações**: Email/SMS quando reserva expira
3. **Relatórios**: Dashboard de vendas, comissões
4. **Multi-tenancy**: Múltiplos empreendimentos
5. **Workflow**: Aprovações, assinaturas digitais
6. **Integração**: CRM, ERP, gateway de pagamento
