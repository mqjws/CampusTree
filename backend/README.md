# CampusTree Backend

FastAPI backend for CampusTree.

## Local Setup

Create database first:

```powershell
createdb -U postgres -h 127.0.0.1 -p 5432 campustree
```

Create virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create local `.env` from `.env.example`, then update `DATABASE_URL`.

Run development server:

```powershell
uvicorn app.main:app --reload
```
