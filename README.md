# Webhook Service - Fast & Modern API 🚀

Um microsserviço moderno, rápido e escalável construído com **FastAPI** para receber e processar webhooks (carrinhos, pedidos, entregas e eventos) e consolidá-los em um banco de dados **SQL Server**. 

O projeto foi modernizado a partir de uma estrutura Flask para adotar os melhores padrões do ecossistema Python moderno, garantindo altíssimo desempenho através do processamento assíncrono.

---

## 🏗️ Arquitetura e Tecnologias

- **Framework Web**: [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn (ASGI) para performance máxima.
- **Gerenciamento de Configuração**: `pydantic-settings` para tipagem estrita de variáveis de ambiente.
- **Banco de Dados**: Microsoft SQL Server.
- **ORM / Drivers**: SQLAlchemy 2.0 e `pyodbc` para operações otimizadas (ex: batch inserts com `fast_executemany`).
- **Background Tasks**: Uso nativo do `BackgroundTasks` do FastAPI para liberar as conexões instantaneamente (status `200 OK`) enquanto os dados são processados e salvos.
- **Containerização**: Docker & Docker Compose com healthchecks, garantindo que a API só inicie quando o banco de dados estiver pronto.

---

## 📂 Estrutura do Projeto

O código-fonte segue a separação de responsabilidades (Clean Architecture style):

```text
webhookservice/
├── app/
│   ├── main.py                  # Entrypoint principal do FastAPI
│   ├── api/
│   │   └── endpoints/           # Rotas da API (ex: webhook.py)
│   ├── core/
│   │   └── config.py            # Validação do .env com Pydantic
│   ├── db/
│   │   ├── database.py          # Conexão com SQL Server (Engine e PyODBC)
│   │   ├── migrations.py        # Criação de tabelas e Seeding automáticos
│   │   ├── models.py            # Definição das tabelas em SQLAlchemy
│   │   └── examples.py          # Exemplos de uso de queries (ORM e Raw SQL)
│   ├── services/                # Lógica de negócio e extração do Payload
│   │   ├── create_cart.py
│   │   ├── create_consignment.py
│   │   ├── create_entries.py
│   │   └── event_history.py
│   ├── SQL/                     # Scripts de inserção/update em lote (Batch)
│   │   └── insert_dim_examples.sql # Script de Seed dos dados dimensionais
│   └── utils/                   # Funções auxiliares (datas, chunking, etc)
├── Dockerfile                   # Configuração da imagem Python otimizada
├── docker-compose.yml           # Orquestração (API + Banco Local)
├── requirements.txt             # Dependências Python
└── .env                         # Variáveis de Ambiente (ver .env.example)
```

---

## ⚙️ Variáveis de Ambiente (`.env`)

A aplicação requer um arquivo `.env` na raiz do projeto. O Pydantic irá validá-lo durante a inicialização.

```ini
user_db=sa
pass_db=Admin123!
host_db=sqlserver_local,1433
db_name=master
```

*(Se alguma variável não estiver definida, a aplicação impedirá a inicialização, evitando falhas silenciosas)*.

---

## 🐳 Como Executar Localmente

Você precisará do **Docker** e **Docker Compose** instalados. 

1. Clone o repositório.
2. Certifique-se de que o arquivo `.env` está configurado corretamente.
3. Suba a aplicação via Docker Compose:

```bash
docker-compose up --build
```

O que acontece durante a execução:
1. O banco `sqlserver_local` é iniciado e o healthcheck aguarda que ele fique pronto.
2. A API FastAPI inicializa.
3. **Auto-Migração**: O `app.db.migrations` verifica se as 25 tabelas do sistema (ex: `CommerceOrders`, `DimEvents`) existem e as cria automaticamente.
4. **Auto-Seed**: Se a tabela `dim_events` estiver vazia, o sistema lê e executa automaticamente o script `insert_dim_examples.sql`, populando as tabelas dimensionais (produtos, lojas, correios, etc) para evitar erros de chave estrangeira.
5. A API fica disponível na porta `5004`:
   - Endpoint Base: `http://localhost:5004`
   - Endpoint dos Webhooks: `POST http://localhost:5004/hook_service/api`

---

## 📡 Endpoints

### Recebimento de Webhooks
`POST /hook_service/api`

Processa de forma unificada os eventos recebidos. A lógica de negócio se divide com base no Header `Ce-Type`:

| Ce-Type Header Regex | Tipo Identificado | Ação Principal |
| :--- | :--- | :--- |
| `*.inboundCartEntry.*` ou `*.inboundOrderEntry.*` | Entries | Insere/Atualiza os Itens (Entries) do Pedido/Carrinho |
| `*.inboundConsignment.*` | Consignment | Atualiza entregas e status de envio |
| `*.inboundCart.*` ou `*.inboundOrder.*` | Cart / Order | Salva Clientes, Endereços de Entrega, Infos de Pagamento e Atualiza o Pedido Master |
| `*.inboundEventHistory.*` | Event History | Salva o histórico de alteração de status do pedido |

**Performance**: O endpoint responde `200 OK` **imediatamente** (em média `< 2ms`), delegando a validação pesada, a transformação JSON e a inserção no banco via PyODBC para processos em segundo plano através do `BackgroundTasks`.

---

## 🛠️ Exemplos de Uso (cURL)

Abaixo um exemplo rápido de como enviar um webhook via `curl`. Para ver a lista completa de payloads para todos os eventos (Carrinho, Consignação, Histórico, etc.), consulte o arquivo dedicado **[WEBHOOK_EXAMPLES.md](./WEBHOOK_EXAMPLES.md)**.

```bash
curl -X POST http://localhost:5004/hook_service/api \
  -H "Content-Type: application/json" \
  -H "Ce-Type: com.example.commercechannel.inboundOrder.v1" \
  -d '{
    "code": "ORDER-12345",
    "customerDocument": "12345678900",
    "customerFirstName": "João",
    "customerLastName": "Silva",
    "customerEmail": "joao@example.com",
    "subtotal": 299.90,
    "status": {
      "code": "CREATED"
    }
  }'
```

---

## 👨‍💻 Desenvolvimento & Scripts Úteis

Se você quiser rodar a aplicação nativamente em sua máquina (sem Docker), certifique-se de ter instalado o driver ODBC 18 for SQL Server.

1. Instale o ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Inicie o servidor:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5005 --reload
```

---

## 📚 Estratégia de Banco de Dados

O banco foi estruturado em um formato híbrido (Modelo Transacional + Star Schema simplificado):
- **Tabelas Dimensionais (`dim_*`)**: Tabelas de referência como `dim_events`, `dim_variantProducts`, `dim_salesChannel`. São populadas automaticamente no boot para não haver inconsistência de Chaves Estrangeiras (FK).
- **Tabelas Fato / Commerce (`Commerce*`)**: Tabelas altamente transacionais populadas diretamente pelos webhooks. 
- **Otimização de Inserção**: O módulo de banco detecta o ODBC e utiliza a flag `fast_executemany = True` do PyODBC, o que aumenta a velocidade de inserts em lote (batch inserts) em até 10x comparado ao SQLAlchemy ORM convencional.

---

> Desenvolvido com foco em velocidade, escalabilidade e arquitetura limpa. 💡
