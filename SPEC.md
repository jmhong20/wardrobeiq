# 👔 WardrobeIQ — Project Specification & Development Roadmap

---

## 1. PROJECT OVERVIEW

**App Name (working title):** WardrobeIQ  
**Type:** Web App (mobile-responsive, PWA-ready)  
**Deployment:** Self-hosted on Ubuntu Home Server  
**Solo Developer:** Yes  
**Goal:** Help users rediscover and utilize their full wardrobe through inventory management and intelligent outfit recommendations.

---

## 2. SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND (React)                  │
│  - Item Upload UI   - Outfit Suggestions             │
│  - Wardrobe Gallery - Stats Dashboard                │
└───────────────────────┬─────────────────────────────┘
                        │ REST API (JSON)
┌───────────────────────▼─────────────────────────────┐
│               BACKEND (FastAPI / Python)             │
│  - Auth Module       - Inventory Service             │
│  - Recommendation Engine (Modular)                   │
│  - Image Processing  - Stats/Analytics Service       │
└──────────┬─────────────────────────┬────────────────┘
           │                         │
┌──────────▼──────────┐   ┌──────────▼──────────────┐
│   MySQL Database    │   │  Image Storage (Local FS │
│  - Users            │   │  or MinIO Object Store)  │
│  - Items            │   └─────────────────────────┘
│  - Outfits          │
│  - Wear Logs        │
└─────────────────────┘
```

**Why this architecture?**
- FastAPI is Python-native (fits your stack), async-ready, and auto-generates API docs
- React gives you a responsive UI that can later become a mobile PWA
- The modular backend cleanly separates concerns so the recommendation engine can be swapped/upgraded independently

---

## 3. DATABASE SCHEMA (MySQL)

```sql
-- Core entities

users(id, username, email, password_hash, created_at)

clothing_items(
  id, user_id, name, image_path,
  category,       -- ENUM: top, bottom, outerwear, shoes, accessory, ...
  style_tags,     -- JSON array: ["streetwear", "casual"]
  color_tags,     -- JSON array: ["navy", "white"]
  season_tags,    -- JSON array: ["summer", "winter"]
  favorability,   -- INT 1-5 (star rating)
  wear_count,     -- INT, auto-incremented
  last_worn,      -- DATE
  active,         -- BOOL (soft delete / retired items)
  created_at
)

outfits(
  id, user_id, name,
  item_ids,       -- JSON array of clothing_item IDs
  source,         -- ENUM: 'manual', 'ai_suggested', 'rule_engine'
  rating,         -- INT 1-5 (user feedback on the outfit)
  created_at
)

wear_logs(
  id, user_id, outfit_id,
  worn_date, weather_context, occasion_tag, notes
)
```

---

## 4. RECOMMENDATION ENGINE (Modular Design)

This is the core intellectual piece of the app. Design it as a **Strategy Pattern** — a pluggable interface where engines are swappable.

```python
# engine/base.py
from abc import ABC, abstractmethod

class RecommendationEngine(ABC):
    @abstractmethod
    def suggest(self, user_id: int, context: dict) -> list[dict]:
        """Returns a list of suggested outfit item combinations."""
        pass
```

### Engine Versions (Upgrade Path)

| Version | Strategy | When to Build |
|---|---|---|
| **v1 — Rule Engine** | Score items by: low wear_count + high favorability + season match | Phase 2 |
| **v2 — Collaborative** | "Users with similar styles also wore..." matrix | Phase 4 |
| **v3 — CV + AI** | Use CLIP/ResNet to auto-tag colors, patterns, style; GPT for outfit narrative | Phase 5 |
| **v4 — LLM Agent** | Chat interface: "I need an outfit for a rainy date night" | Phase 6 |

### v1 Scoring Formula (Rule Engine)
```
score(item) =
  (favorability × 0.4)
  + (recency_penalty × 0.35)    # higher score if not worn recently
  + (season_match × 0.15)
  + (style_cohesion × 0.10)     # items in outfit share style_tags
```

---

## 5. DEVELOPMENT ROADMAP

### ✅ PHASE 0 — Foundation (Week 1–2)
**Goal:** Project skeleton, dev environment, CI basics

- [ ] Create Git repo (GitHub/Gitea on home server)
- [ ] Set up Ubuntu Server: Python venv, MySQL, Nginx
- [ ] Scaffold FastAPI project structure
- [ ] Scaffold React app with Vite
- [ ] Set up `.env` config management
- [ ] Initialize MySQL schema (use Alembic for migrations)
- [ ] Docker Compose file for local dev (optional but recommended)

**Deliverable:** "Hello World" frontend talking to backend API

---

### 📦 PHASE 1 — Inventory Core (Week 3–5)
**Goal:** Users can add, view, and manage clothing items

- [ ] User auth (JWT — register/login/logout)
- [ ] Image upload endpoint (store to local filesystem or MinIO)
- [ ] CRUD API for clothing_items
- [ ] React: Wardrobe gallery page (grid view of items)
- [ ] React: Add item form (photo upload + metadata tagging)
- [ ] React: Item detail/edit page

**Deliverable:** Fully functional wardrobe inventory

---

### 🌟 PHASE 2 — Data Tracking + Rule Engine (Week 6–9)
**Goal:** Track usage data and generate first outfit suggestions

- [ ] "Log a wear" feature — ties an outfit to a date
- [ ] Wear count + last_worn auto-update on log
- [ ] Favorability rating UI (star widget)
- [ ] Build v1 Rule Engine (see scoring formula above)
- [ ] Outfit suggestion API endpoint
- [ ] React: "Suggest an Outfit" page
- [ ] React: Outfit card UI (shows item thumbnails together)
- [ ] User can accept/reject/rate suggestions → feeds back into scoring

**Deliverable:** Working recommendation loop

---

### 📊 PHASE 3 — Dashboard & Analytics (Week 10–12)
**Goal:** Give users insight into their wardrobe behavior

- [ ] Stats API: most worn, never worn, cost-per-wear (if prices added), style breakdown
- [ ] React: Dashboard with charts (Recharts or Chart.js)
- [ ] "Wardrobe gaps" suggestion (e.g., "You have 12 tops but only 2 bottoms")
- [ ] Outfit history calendar view
- [ ] Export wardrobe data (CSV/JSON)

**Deliverable:** Insight dashboard — the "wow" feature for users

---

### 🔧 PHASE 4 — Polish & PWA (Week 13–15)
**Goal:** Make it production-quality and mobile-friendly

- [ ] Make React app a PWA (manifest + service worker)
- [ ] Mobile-responsive UI audit
- [ ] Performance: lazy loading images, pagination
- [ ] HTTPS via Let's Encrypt (Nginx config)
- [ ] User settings page (profile, notification preferences)
- [ ] Basic automated tests (pytest for API, React Testing Library for UI)

**Deliverable:** Deployable v1.0

---

### 🤖 PHASE 5 — AI Upgrade (Future)
**Goal:** Swap in AI-powered recommendation engine (modular swap)

- [ ] Integrate CLIP model for auto-tagging images (color, pattern, category)
- [ ] Style embedding vectors — find "similar" items mathematically
- [ ] Outfit coherence scoring using visual similarity
- [ ] Swap RecommendationEngine implementation — zero disruption to API contract

---

## 6. TECHNOLOGY STACK (Complete)

### ✅ You Already Know
| Tech | Role |
|---|---|
| Python | Backend logic, scripting |
| Anaconda | Environment management |
| MySQL | Primary database |
| Ubuntu Server | Hosting platform |

### 📚 New Technologies to Learn

| Technology | Role | Priority | Learning Curve |
|---|---|---|---|
| **FastAPI** | Python web framework for REST API | 🔴 Critical | Low — very Pythonic |
| **SQLAlchemy** | Python ORM for MySQL | 🔴 Critical | Low-Medium |
| **Alembic** | Database migration tool (pairs with SQLAlchemy) | 🔴 Critical | Low |
| **React (+ Vite)** | Frontend UI framework | 🔴 Critical | Medium |
| **JWT Auth** | Stateless user authentication | 🔴 Critical | Low |
| **Nginx** | Reverse proxy + static file server | 🟠 Important | Low |
| **Docker / Docker Compose** | Containerized dev environment | 🟠 Important | Medium |
| **MinIO** | S3-compatible local object storage for images | 🟡 Optional | Low |
| **Pydantic** | Data validation (built into FastAPI) | 🔴 Critical | Low |
| **Pytest** | Backend testing | 🟠 Important | Low |
| **Pillow (PIL)** | Python image processing (resize/compress uploads) | 🟠 Important | Low |
| **Recharts / Chart.js** | Frontend data visualization | 🟡 Optional | Low |
| **CLIP (OpenAI)** | AI image understanding for Phase 5 | 🟢 Future | Medium-High |

### Recommended Learning Order
```
FastAPI → SQLAlchemy/Alembic → React basics →
JWT Auth → Nginx → Docker → (Pillow, Pydantic along the way)
```

---

## 7. FOLDER STRUCTURE

```
wardrobeiq/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── models/              # SQLAlchemy DB models
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── routers/             # API route handlers
│   │   │   ├── auth.py
│   │   │   ├── items.py
│   │   │   ├── outfits.py
│   │   │   └── recommendations.py
│   │   ├── engine/              # Recommendation engine (modular)
│   │   │   ├── base.py          # Abstract base class
│   │   │   ├── rule_engine.py   # v1
│   │   │   └── ai_engine.py     # v3 (future)
│   │   ├── services/            # Business logic layer
│   │   └── core/                # Config, auth utils, db connection
│   ├── tests/
│   ├── alembic/                 # DB migrations
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── api/                 # Axios API client
│   └── package.json
│
├── docker-compose.yml
└── README.md
```

---

## 8. KEY RISKS & MITIGATIONS

| Risk | Mitigation |
|---|---|
| Scope creep on recommendation engine | Build v1 rule engine first; don't touch AI until v1 ships |
| Image storage growing large | Compress on upload (Pillow), set max resolution (e.g., 800px) |
| MySQL query performance on large wardrobes | Index on user_id, category, last_worn from day one |
| Frontend complexity overwhelming solo dev | Use a component library (shadcn/ui or Chakra UI) to move fast |
| Losing motivation mid-project | Ship Phase 1 fast — having real data in the app is highly motivating |

---

*Generated with Claude — WardrobeIQ Project Specification v1.0*
