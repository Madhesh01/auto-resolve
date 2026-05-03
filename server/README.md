# auto-resolve — server

FastAPI backend, background worker, and AI agent for automatically classifying and resolving customer support tickets.

## How it works

1. User submits a support ticket via `POST /ticket`
2. Ticket is saved to PostgreSQL and pushed to a Redis queue
3. A background worker picks up the ticket and passes it to the LangChain agent
4. The agent selects the appropriate tool, executes it, and synthesizes a resolution
5. The ticket is updated in PostgreSQL with the status and AI-generated response

```
POST /ticket → PostgreSQL (Pending) → Redis Queue → Worker → Agent → Tool → PostgreSQL (Resolved/Flagged/Needs Info)
```

## Tech Stack

- **Backend** — FastAPI
- **Database** — PostgreSQL with SQLAlchemy (async)
- **Queue** — Redis
- **AI** — LangChain agent over Ollama (local) or Google Gemini (cloud), swapped via `LLM_PROVIDER`

## Project Structure

```
server/
├── app/
│   ├── main.py                 # FastAPI app entry point + CORS + lifespan
│   ├── db.py                   # Async SQLAlchemy engine and session
│   ├── redis.py                # Async Redis client
│   ├── llm.py                  # LangChain wrapper — Ollama or Gemini via LLM_PROVIDER
│   ├── agents/
│   │   └── ticket_agent.py     # LangChain agent with tools attached
│   ├── routes/
│   │   └── tickets.py          # POST /ticket, GET /ticket/{id}/status, GET /tickets
│   ├── models/
│   │   ├── ticket.py           # SQLAlchemy Ticket model
│   │   └── order.py            # SQLAlchemy Order model
│   ├── schemas/
│   │   └── ticket.py           # Pydantic schemas
│   ├── services/
│   │   └── ticket_service.py   # insert_ticket, update_ticket, get_ticket_status, get_tickets
│   └── tools/
│       └── order_tools.py      # get_order_status, cancel_order, update_shipping_address
├── worker/
│   └── main.py                 # BLPOP loop → agent → DB update
├── init.sql                    # Seeds orders table on first postgres boot
├── test_pipeline.py            # Async load test script
└── requirements.txt
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/ticket` | Submit a new support ticket |
| `GET` | `/ticket/{id}/status` | Poll ticket status and AI resolution |
| `GET` | `/tickets` | Fetch all tickets |

### POST /ticket

```json
{
  "case_title": "Cancel my order",
  "case_owner": "John",
  "case_description": "Please cancel my order number 40",
  "case_status": "Pending"
}
```

### GET /ticket/{id}/status

```json
{
  "status": "Resolved",
  "ai_resolution": "Order #40 has been successfully cancelled."
}
```

## Ticket Statuses

| Status | Description |
|--------|-------------|
| `Pending` | Ticket received, queued for processing |
| `Resolved` | Tool executed successfully |
| `Flagged` | Tool ran but encountered an error (e.g. order not found) |
| `Needs Info` | Agent could not extract enough information to act |

## Available Tools

| Tool | Description |
|------|-------------|
| `get_order_status` | Returns the current status of an order |
| `cancel_order` | Cancels an order |
| `update_shipping_address` | Updates the shipping address of an order |

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL
- Redis
- Ollama (if using `LLM_PROVIDER=ollama`) or a Gemini API key

### Installation

```bash
cd server
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file inside `server/`:

```
DATABASE_URL=postgresql+asyncpg://postgres:<password>@localhost:5432/autoresolve
REDIS_URL=redis://localhost:6379

# LLM — set to "ollama" or "gemini"
LLM_PROVIDER=gemini
GEMINI_API_KEY=<your key>
GEMINI_MODEL=gemini-2.5-flash-lite

# Only needed when LLM_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
```

### Running

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Start the worker in a separate terminal:

```bash
python worker/main.py
```

### Load testing

```bash
python test_pipeline.py    # default: 20 tickets, edit N at the top to change
```
