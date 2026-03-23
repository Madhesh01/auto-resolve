# auto-resolve

An AI-powered customer support dashboard that automatically classifies and resolves support tickets using Google Gemini, FastAPI, PostgreSQL, and Redis. Built from a team lead's perspective — log cases on behalf of customers and let auto-resolve handle the rest in real time.

## How it works

1. Team lead submits a support ticket via the React dashboard
2. Ticket is saved to PostgreSQL and pushed to a Redis queue
3. A background worker picks up the ticket and sends it to Gemini for intent classification
4. Gemini selects the most appropriate tool and extracts order details from the description
5. The tool executes against PostgreSQL and the ticket is updated with the resolution
6. The dashboard polls for status updates and reflects the result in real time

```
New Case (React) → POST /ticket → PostgreSQL (Pending) → Redis Queue → Worker → Gemini → Tool → PostgreSQL (Resolved/Flagged/Needs Info) → Dashboard updates
```

## Tech Stack

- **Frontend** — React + Tailwind CSS (Vite)
- **Backend** — FastAPI
- **Database** — PostgreSQL with SQLAlchemy (async)
- **Queue** — Redis
- **AI** — Google Gemini 2.0 Flash
- **Containerization** — Docker (in progress)

## Project Structure

```
auto-resolve/
├── client/                         # React frontend
│   ├── src/
│   │   ├── App.jsx                 # Root component, state management, polling
│   │   ├── main.jsx                # React entry point
│   │   ├── index.css               # Tailwind import
│   │   └── components/
│   │       ├── CaseQueue.jsx       # Ticket list with filter tabs + empty state
│   │       ├── CreateCaseModal.jsx # New ticket form with simulate button
│   │       └── CaseDetailModal.jsx # Ticket detail + AI resolution display
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
└── server/                         # FastAPI backend
    ├── app/
    │   ├── main.py                 # FastAPI app entry point + CORS
    │   ├── db.py                   # SQLAlchemy async engine and session
    │   ├── redis.py                # Redis client
    │   ├── gemini.py               # Gemini intent classification
    │   ├── routes/
    │   │   └── tickets.py          # API route definitions
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
    │   └── main.py                 # Redis consumer loop + tool execution
    ├── requirements.txt
    └── docker-compose.yml
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
- Node.js 18+
- PostgreSQL
- Redis

### Backend setup

```bash
git clone https://github.com/yourusername/auto-resolve.git
cd auto-resolve/server

python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the root:

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/autoresolve
REDIS_URL=redis://localhost:6379
GEMINI_API_KEY=your_gemini_api_key
```

### Database setup

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

### Frontend setup

```bash
cd auto-resolve/client
npm install
```

## Running

Start the FastAPI server:

```bash
cd server
source env/bin/activate
uvicorn app.main:app --reload
```

Start the background worker:

```bash
cd server
source env/bin/activate
python worker/main.py
```

Start the React frontend:

```bash
cd client
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## Roadmap

- [x] FastAPI backend with PostgreSQL and Redis queue
- [x] Gemini-powered intent classification and tool execution
- [x] React dashboard with real-time status polling
- [x] Dark mode
- [ ] systemd service for background worker
- [ ] Docker + docker-compose for one-command setup
- [ ] Support for more tools (refund, escalation, FAQ lookup)
- [ ] pgvector for semantic ticket deduplication
- [ ] Authentication for team lead access