# DevOps Platform

A comprehensive DevOps platform built with **Python FastAPI** (backend) and **React + TypeScript** (frontend), providing CI/CD pipeline management, build tracking, deployment management, service registry, and environment management.

## Features

- 🔐 **JWT Authentication** — Secure login with role-based access (admin, developer, viewer)
- ⚡ **Pipeline Management** — Create and trigger CI/CD pipelines with push/PR/manual/schedule triggers
- 🔨 **Build History** — Track build status, logs, and duration per pipeline
- 🚀 **Deployment Management** — Manage deployments across environments with rollback support
- 🔧 **Service Registry** — Register and manage microservices with metadata
- 🌍 **Environment Management** — Manage dev, staging, and production environments
- 📊 **Dashboard** — Overview stats and recent activity feed

## Architecture

```
.
├── backend/          # Python FastAPI + SQLAlchemy + SQLite
│   ├── app/
│   │   ├── main.py         # FastAPI app with CORS + seeding
│   │   ├── database.py     # SQLAlchemy SQLite setup
│   │   ├── models.py       # ORM models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── auth.py         # JWT auth helpers
│   │   └── routers/        # API route handlers
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/         # React + TypeScript + Vite + Tailwind CSS
│   ├── src/
│   │   ├── App.tsx         # React Router setup
│   │   ├── api/            # Axios client + API functions
│   │   ├── components/     # Layout, StatCard
│   │   ├── pages/          # Dashboard, Pipelines, Builds, etc.
│   │   └── types/          # TypeScript interfaces
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

## Quick Start

### Option 1: Docker Compose (recommended)

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

**Backend:**

```bash
cd backend
pip install -r requirements.txt
mkdir -p data
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

The frontend dev server runs on http://localhost:3000 and proxies `/api` requests to the backend.

## Demo Credentials

| Username    | Password   | Role      |
|-------------|------------|-----------|
| `admin`     | `admin123` | admin     |
| `developer` | `dev123`   | developer |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/login` | Login, returns JWT token |
| `POST` | `/api/auth/register` | Register new user |
| `GET`  | `/api/dashboard/stats` | Dashboard overview |
| `GET/POST` | `/api/services/` | List / create services |
| `GET/PUT/DELETE` | `/api/services/{id}` | Service CRUD |
| `GET/POST` | `/api/environments/` | List / create environments |
| `GET/PUT/DELETE` | `/api/environments/{id}` | Environment CRUD |
| `GET/POST` | `/api/pipelines/` | List / create pipelines |
| `POST` | `/api/pipelines/{id}/trigger` | Manually trigger a pipeline |
| `GET/POST` | `/api/builds/` | List / create builds |
| `GET` | `/api/builds/{id}` | Get build details |
| `GET/POST` | `/api/deployments/` | List / create deployments |
| `POST` | `/api/deployments/{id}/rollback` | Rollback a deployment |
| `GET` | `/health` | Health check |

Full interactive API docs available at http://localhost:8000/docs

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, FastAPI, SQLAlchemy, SQLite |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Frontend | React 18, TypeScript, Vite |
| Styling | Tailwind CSS (CDN) |
| HTTP Client | Axios |
| Routing | React Router v6 |
| Containerization | Docker, Docker Compose, Nginx |
