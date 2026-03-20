
auto-resolve/
├── app/
│   ├── main.py
│   ├── routes/
│   ├── models/
│   ├── schemas/
│   └── services/
├── worker/
├── .env
└── docker-compose.yml


- `routes/` — your two API endpoints (one for webhook, and one for polling)
- `models/` — SQLAlchemy database tables
- `schemas/` — Pydantic request/response models
- `services/` — business logic, Redis interaction, DB queries
- `worker/` — background worker, Redis blpop loop, LLM orchestration, FastMCP tool calls

