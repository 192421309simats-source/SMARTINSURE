# SmartInsure (Local Demo)

Local demo of SmartInsure static frontend + FastAPI backend (recommendation engine + admin endpoints).

Requirements
- Python 3.10+ (tested with 3.14)

Setup

1. Create and activate a virtual environment (recommended):

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install Python dependencies:

```powershell
py -3 -m pip install -r requirements.txt
```

3. Seed the database:

```powershell
py -3 -m scripts.seed_db
```

4. Start the static front-end (serve workspace root):

```powershell
py -3 -m http.server 8000
```

5. Start the API server:

```powershell
py -3 -m uvicorn app.main:app --reload --port 8001
```

Admin token (demo)
- The backend protects admin endpoints with a header `X-Admin-Token`.
- Default demo token: `admin-secret` (set env `SMARTINSURE_ADMIN_TOKEN` to change it).

Purchase flow
- Use the recommendations page to view a policy and click "Buy Now". The demo will prompt for name and email and create a record in the `purchases` table inside `smartinsure.db` via `POST /api/purchase`.

Notes
- Recommendations are rule-based in `app/main.py` (`POST /api/profile`).
- Admin endpoints: `/api/admin/*`.
- The front-end calls `http://127.0.0.1:8001` by default; adjust if running API on another host/port.

Render deployment (single service)

1. Commit your repo to GitHub.
2. On Render, create a new "Web Service", connect your GitHub repo, and select the branch.
3. Render will detect the `Dockerfile` and build the image. Ensure the service uses port `8000` or that the start command uses `$PORT`.
4. (Optional) Set environment variable `SMARTINSURE_ADMIN_TOKEN` in Render's dashboard to override the admin token.
5. Deploy — the FastAPI service will serve both the API and the static frontend from the same container.

Notes about persistence: this demo uses SQLite (`smartinsure.db`). Render's filesystem is ephemeral across deploys; for persistent data, use Render Postgres and update `app/main.py` to use Postgres instead of SQLite.
