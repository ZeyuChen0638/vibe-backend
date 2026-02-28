# Backend

FastAPI + PostgreSQL backend for Vibe Platform.

## Setup

```bash
conda activate vibe-code
cd /home/owen/vibe-plt/backend
python -m pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /api/health`
- `GET /api/db`
