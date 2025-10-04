# Carbon Credit Ledger API

**Tech Stack:** FastAPI, PostgreSQL, Alembic (for migrations), SQLAlchemy

---

## Project Overview

This API manages carbon credits with a simple lifecycle: `CREATED → SOLD → RETIRED`.
Each credit is immutable and tracked through an **event log**, so every action is recorded without modifying the original record.
IDs are deterministic, ensuring that the same input always generates the same UUID.

---

## API Endpoints

* **POST /register/** → Register or create a credit.
* **POST /records/{id}/retire** → Retire a credit using its ID.
* **GET /records/{id}** → Retrieve full record details along with its history/events.

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/vishal160204/Backend-Exercise
cd Backend-Exercise
```

2. **Create a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure the database**

* Set the database URL in `alembic.ini` and `database/sessions.py`.

5. **Run migrations**

```bash
alembic upgrade head
```

6. **Start the FastAPI server**

```bash
uvicorn main:app --reload
```

---

## Example Requests

**Create a Credit**

```bash
POST /register/
Content-Type: application/json

{
  "project_name": "Project ",
  "registry": "Registry1",
  "vintage": "2023",
  "quantity": 100,
  "serial_number": "SN1234"
}
```

**Retire a Credit**

```bash
POST /records/{id}/retire/
```

**Get Credit Details**

```bash
GET /records/{id}/
```

---

## Reflection Questions

**Q1: How did you design the ID so it’s always the same for the same input?**
A: We generate a deterministic UUIDv5 from key credit fields (`project_name`, `registry`, `vintage`, `quantity`). This ensures that the same input always produces the same ID, preventing duplicates.

**Q2: Why did you use an event log instead of updating the record directly?**
A: The event log preserves an immutable  history. Each action (`CREATED`, `SOLD`, `RETIRED`) is stored as a separate event, allowing full auditability, easy tracking, and preventing accidental overwrites.

**Q3: If two people tried to retire the same credit at the same time, what would break?**
A: A race condition could occur: both users might see the last event as `SOLD` and insert a `RETIRED` event simultaneously, creating duplicates and breaking lifecycle rules.

**Q4: How would you fix it?**
A: we can  enforce a unique database constraint on the (record_id, event_type) columns of the Events table, which would prevent the insertion of a duplicate RETIRED event..


