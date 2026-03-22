# auto-resolve
An AI-powered customer support agent that automatically classifies and resolves support tickets using Google Gemini, FastAPI, PostgreSQL, and Redis.

## How it works

1. Customer submits a support ticket via `POST /ticket`
2. Ticket is saved to PostgreSQL and pushed to a Redis queue
3. A background worker picks up the ticket and sends it to Gemini for intent classification
4. Gemini selects the most appropriate tool and extracts order details from the ticket description
5. The tool executes against PostgreSQL and the ticket is updated with the resolution

```
POST /ticket → PostgreSQL (Pending) → Redis Queue → Worker → Gemini → Tool → PostgreSQL (Resolved)
```

## Tech Stack

- **Backend** — FastAPI
- **Database** — PostgreSQL with SQLAlchemy (async)
- **Queue** — Redis
- **AI** — Google Gemini 2.0 Flash
- **Frontend** — React + Tailwind (in progress)
- **Containerization** — Docker (in progress)

## Project Structure

```
auto-resolve/
├── app/
│   ├── main.py               # FastAPI app entry point
│   ├── db.py                 # SQLAlchemy async engine and session
│   ├── redis.py              # Redis client
│   ├── gemini.py             # Gemini intent classification
│   ├── routes/
│   │   └── tickets.py        # POST /ticket, GET /ticket/{id}/status
│   ├── models/
│   │   ├── ticket.py         # SQLAlchemy Ticket model
│   │   └── order.py          # SQLAlchemy Order model
│   ├── schemas/
│   │   └── ticket.py         # Pydantic schemas
│   ├── services/
│   │   └── ticket_service.py # insert_ticket, update_ticket, get_ticket_status
│   └── tools/
│       └── order_tools.py    # get_order_status, cancel_order, update_shipping_address
├── worker/
│   └── main.py               # Redis consumer loop + tool execution
├── .env
└── docker-compose.yml
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ticket` | Submit a new support ticket |
| GET | `/ticket/{id}/status` | Poll ticket status and resolution |

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
  "status": "Resolved"
}
```

## Ticket Statuses

| Status | Description |
|--------|-------------|
| `Pending` | Ticket received, queued for processing |
| `Resolved` | Tool executed successfully |
| `Flagged` | Tool executed but encountered an error (e.g. order not found) |
| `Needs Info` | Gemini could not extract enough information to act |

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

### Installation

```bash
git clone https://github.com/yourusername/auto-resolve.git
cd auto-resolve
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/autoresolve
REDIS_URL=redis://localhost:6379
GEMINI_API_KEY=your_gemini_api_key
```

### Database Setup

```sql
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    owner VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    ai_resolution VARCHAR
);

CREATE TABLE orders (
    order_no INT PRIMARY KEY,
    address VARCHAR NOT NULL,
    status VARCHAR NOT NULL
);
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

## Roadmap

- [ ] React frontend with ticket submission and status polling
- [ ] Docker + docker-compose for one-command setup
- [ ] Support for more tools (refund, escalation, FAQ lookup)
- [ ] pgvector for semantic ticket deduplication
