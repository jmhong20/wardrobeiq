# WardrobeIQ

Intelligent wardrobe management & outfit recommendations.
Self-hosted on Ubuntu · FastAPI backend · React + Vite frontend · MySQL

---

## Quick Start (Docker)

```bash
# 1. Copy env file
cp .env.example backend/.env
# Edit backend/.env and set a real SECRET_KEY

# 2. Start everything
docker compose up --build

# 3. Open in browser
#   Frontend:  http://localhost:5173
#   API docs:  http://localhost:8000/docs
```

The `backend` container automatically runs `alembic upgrade head` on startup to
apply all migrations before the server starts.

---

## Local Dev (no Docker)

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # set DATABASE_URL to your local MySQL

alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite proxies `/api/*` → `http://localhost:8000` automatically.

---

## Running Tests

```bash
cd backend
pytest tests/ -v
```

---

## Project Structure

```
wardrobeiq/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── routers/             # Route handlers (auth, items, outfits, recommendations)
│   │   ├── engine/              # Pluggable recommendation engine
│   │   │   ├── base.py          # Abstract Strategy interface
│   │   │   ├── rule_engine.py   # v1 scoring engine (Phase 2)
│   │   │   └── ai_engine.py     # v3 CLIP/LLM stub (Phase 5)
│   │   ├── services/            # Business logic
│   │   └── core/                # Config, DB session, JWT security
│   ├── tests/
│   ├── alembic/                 # DB migrations
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/client.js        # Axios wrapper with JWT interceptor
│   │   ├── pages/Home.jsx       # Phase 0 landing page
│   │   ├── components/          # Shared UI components (Phase 1+)
│   │   └── hooks/               # Custom React hooks (Phase 1+)
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml
└── .env.example
```

---

## Roadmap

| Phase | Goal | Status |
|-------|------|--------|
| 0 | Foundation skeleton | ✅ Done |
| 1 | Inventory CRUD + image upload | 🔜 Next |
| 2 | Wear tracking + Rule Engine | ⏳ Planned |
| 3 | Dashboard & analytics | ⏳ Planned |
| 4 | PWA + production hardening | ⏳ Planned |
| 5 | CLIP/LLM recommendation upgrade | 🔮 Future |

---

*Generated from WardrobeIQ Project Specification v1.0*
