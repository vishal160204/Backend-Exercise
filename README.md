# Carbon Credit Ledger API

Tech Stack: FastAPI, PostgreSQL, Alembic(for migration), SQLAlchemy

---

## API Endpoints

POST /register/ -> register or create  credits 

POST /records/{id}/retire  -> retire credit using id

GET /records/{id}         -> get record complete details its history or events




## Installation

1. **Clone Repo**
```bash
git clone https://github.com/yourusername/carbon-credits-api.git
cd carbon-credits-api

Create Virtual Environment

python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

Install dependency

pip install -r requirements.txt

set database url in alembic.ini and database/session.py/  

run migration

alembic upgrade head

start server

fastapi dev main.py




