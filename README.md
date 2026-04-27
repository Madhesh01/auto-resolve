# auto-resolve

An AI-powered customer support dashboard that automatically classifies and resolves support tickets. Built from a user's perspective — log cases on behalf of customers and let auto-resolve handle the rest in real time.

The LLM layer is provider-agnostic via LangChain: swap between local inference (Ollama) and cloud (Google Gemini) with a single env variable. The full stack runs on Docker and is deployed on AWS EC2.

## How it works

1. User submits a support ticket via the React dashboard
2. Ticket is saved to PostgreSQL and pushed to a Redis queue
3. A background worker picks up the ticket and sends it to the LLM for intent classification
4. The LLM selects the most appropriate tool and extracts order details from the description
5. The tool executes against PostgreSQL and the ticket is updated with the resolution
6. The dashboard polls for status updates and reflects the result in real time

```
New Case (React) → POST /ticket → PostgreSQL (Pending) → Redis Queue → Worker → LLM → Tool → PostgreSQL (Resolved/Flagged/Needs Info) → Dashboard updates
```

## Tech Stack

- **Frontend** — React + Tailwind CSS (Vite), served by nginx
- **Backend** — FastAPI
- **Database** — PostgreSQL with SQLAlchemy (async)
- **Queue** — Redis
- **AI** — LangChain abstraction over Google Gemini 2.5 Flash Lite (cloud) or Ollama/qwen2.5:7b (local)
- **Reverse Proxy** — nginx
- **Containerization** — Docker + docker-compose
- **Deployment** — AWS EC2 (t3.small, Ubuntu 24.04)

## Performance

Load tested with 20–100 concurrent tickets using a custom async test script (`server/test_pipeline.py`):

| Metric | Result |
|--------|--------|
| Ingestion throughput | ~93 tickets/sec |
| LLM inference latency (Ollama, qwen2.5:7b) | 0.65s avg |
| End-to-end latency (submit → resolved) | ~2–3s |
| Redis queue peak depth (100 tickets) | 73 |
| Throughput gain with 2 workers | 1.8x vs 1 worker |

Workers scale horizontally — both BLPOP the same Redis queue independently.

## Project Structure

```
auto-resolve/
├── docker-compose.yml              # Orchestrates all 5 services
├── .env.example                    # Environment variable template
│
├── client/                         # React frontend
│   ├── src/
│   │   ├── App.jsx                 # All state + polling logic
│   │   ├── main.jsx
│   │   ├── index.css
│   │   └── components/
│   │       ├── CaseQueue.jsx       # Filterable ticket list
│   │       ├── CreateCaseModal.jsx # New ticket form with simulate button
│   │       └── CaseDetailModal.jsx # Ticket detail + AI resolution display
│   ├── nginx.conf                  # nginx config (static files + /api proxy)
│   ├── Dockerfile.client           # Multi-stage: node builder → nginx
│   ├── vite.config.js              # /api proxy for local dev
│   └── package.json
│
└── server/                         # FastAPI backend + worker
    ├── Dockerfile.server           # python:3.11-slim; CMD overridden for worker
    ├── init.sql                    # Seeds orders table on first postgres boot
    ├── test_pipeline.py            # Async load test script
    ├── requirements.txt
    └── app/
        ├── main.py                 # FastAPI app + CORS + lifespan
        ├── db.py                   # Async SQLAlchemy engine
        ├── redis.py                # Async Redis client
        ├── llm.py                  # LangChain wrapper — Ollama or Gemini via LLM_PROVIDER
        ├── models/
        │   ├── ticket.py           # tickets table ORM
        │   └── order.py            # orders table ORM
        ├── schemas/ticket.py       # Pydantic Ticket + CaseStatus
        ├── routes/tickets.py       # POST /ticket, GET /ticket/{id}/status, GET /tickets
        ├── services/
        │   └── ticket_service.py   # All DB reads/writes + queue push
        ├── tools/
        │   └── order_tools.py      # get_order_status, cancel_order, update_shipping_address
        └── worker/
            └── main.py             # BLPOP loop → LLM → tool → DB update
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/ticket` | Submit a new support ticket |
| `GET` | `/ticket/{id}/status` | Poll ticket status and AI resolution |
| `GET` | `/tickets` | Fetch all tickets for the queue |

### POST /ticket — Request body

```json
{
  "case_title": "Cancel my order",
  "case_owner": "Sarah Kim",
  "case_description": "Please cancel order number 40",
  "case_status": "Pending"
}
```

### GET /ticket/{id}/status — Response

```json
{
  "status": "Resolved",
  "ai_resolution": "Order #40 has been successfully cancelled."
}
```

### GET /tickets — Response

```json
[
  {
    "case_id": 1,
    "case_title": "Cancel my order",
    "case_owner": "Sarah Kim",
    "case_description": "Please cancel order number 40",
    "case_status": "Resolved",
    "ai_resolution": "Order #40 has been successfully cancelled."
  }
]
```

## Ticket Statuses

| Status | Description |
|--------|-------------|
| `Pending` | Ticket received, queued for processing |
| `Resolved` | Tool executed successfully |
| `Flagged` | Tool ran but encountered an error (e.g. order not found) |
| `Needs Info` | LLM could not extract enough information to act |

## Available Tools

| Tool | Description |
|------|-------------|
| `get_order_status` | Returns the current status of an order |
| `cancel_order` | Cancels an order |
| `update_shipping_address` | Updates the shipping address of an order |

## Setup

### Option A — Docker (recommended)

Requires Docker and docker-compose.

```bash
git clone https://github.com/yourusername/auto-resolve.git
cd auto-resolve
cp .env.example .env
# Fill in POSTGRES_PASSWORD and GEMINI_API_KEY (or set LLM_PROVIDER=ollama)
docker compose up --build
```

Open [http://localhost](http://localhost) in your browser.

### Option B — Local dev

**Prerequisites:** Python 3.11+, Node.js 18+, PostgreSQL, Redis

**Backend:**

```bash
cd server
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

**Frontend:**

```bash
cd client
npm install
```

## Environment Variables

Create a `.env` file in `server/` for local dev, or at the project root for Docker:

```
# Database
DATABASE_URL=postgresql+asyncpg://postgres:<password>@localhost:5432/autoresolve
POSTGRES_PASSWORD=<password>

# Redis
REDIS_URL=redis://localhost:6379

# LLM — set to "ollama" or "gemini"
LLM_PROVIDER=gemini
GEMINI_API_KEY=<your key>
GEMINI_MODEL=gemini-2.5-flash-lite

# Only needed when LLM_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
```

## Running (local dev)

Three processes must run simultaneously in separate terminals:

```bash
# Terminal 1 — FastAPI server
cd server && source env/bin/activate
uvicorn app.main:app --reload          # http://localhost:8000

# Terminal 2 — Background worker
cd server && source env/bin/activate
python worker/main.py

# Terminal 3 — React dev server
cd client && npm run dev               # http://localhost:5173
```

## Load Testing

```bash
cd server
source env/bin/activate
python test_pipeline.py                # default: 20 tickets
```

Edit `N` at the top of the script to change ticket count.

## Roadmap

- [x] FastAPI backend with PostgreSQL and Redis queue
- [x] LangChain abstraction — swap Ollama and Gemini via env var
- [x] Async load testing with real metrics
- [x] React dashboard with real-time status polling
- [x] Dark mode
- [x] Docker + docker-compose for one-command setup
- [x] AWS EC2 deployment behind nginx
- [ ] Elastic IP for stable public URL
- [ ] GitHub Actions + DockerHub CI/CD pipeline
- [ ] Support for more tools (refund, escalation, FAQ lookup)
- [ ] pgvector for semantic ticket deduplication
- [ ] Authentication for user access
