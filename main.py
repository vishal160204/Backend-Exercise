from fastapi import FastAPI,HTTPException,Depends
from utils.hashing import uuid_generate
from schemas.carbon_credits import RegisterCredit
from database.sessions import get_db
from database.db import Base
from sqlalchemy.orm import Session
from models.credits import Events,Credits

app = FastAPI()

@app.post("/register/")
def create_credit(credit_data : RegisterCredit, db : Session = Depends(get_db)):
    record_id = uuid_generate(credit_data)
    try:
        check_existing = db.query(Credits).filter_by(id=record_id).first()
        if check_existing:
            raise HTTPException(status_code = 400, detail = "credit already registered.")

        new_credit = Credits(
            id = record_id,
            project_name = credit_data.project_name,
            registry = credit_data.registry,
            vintage = credit_data.vintage,
            quantity = credit_data.quantity,
            serial_number = credit_data.serial_number
        )
        created_event = Events(record_id=record_id, event_type="CREATED")
        db.add(new_credit)

        db.add(created_event)
        db.commit()
        db.refresh(new_credit)
        db.refresh(created_event)
        return {"message": "Credit Created Successfully."}
    except HTTPException:  # Don't override your own error
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code = 400, detail = "credit creation failed.")
    

@app.post("/records/{id}/retire/")
def retire_credit(record_id : str, db : Session = Depends(get_db)):
    check_credit = db.query(Credits).filter_by(id = record_id).first()
    if not check_credit:
        raise HTTPException(status_code = 404, detail = "Credit not found.")
    
    last_event = db.query(Events).filter(Events.record_id == record_id).order_by(Events.timestamp.desc()).first()

    if not last_event or last_event.event_type != "sold":
        raise HTTPException(status_code = 400, detail = "Credit must be sold befoer retiring.")
    if last_event.event_type =="Retired":
        raise HTTPException(status_code=400, detail="Credit already Retired.")
    event = Events(
        record_id = record_id,
        event_type = "Retired"
    )
    db.add(event)
    db.commit()
    db.refresh(events_record)
    return {"message" : "Credit Successfully Retired"}

@app.get("/record/{record_id}/")
def get_record(record_id : str, db : Session = Depends(get_db)):
    check_credit = db.query(Credits).filter_by(id  = record_id).first()
    if not check_credit:
        raise HTTPException(status_code = 404, detail = " credit not found,")
    events = db.query(Events).filter_by(record_id = record_id).order_by(Events.timestamp.asc()).all()
    return {
        "credit" : {
            "id" : check_credit.id,
            "project_name" : check_credit.project_name,
            "registry" : check_credit.registry,
            "vintage" : check_credit.vintage,
            "quantity" : check_credit.quantity,
            "serial number" : check_credit.serial_number
        },
        "history" : [{"event_type" : e.event_type, "timestamp" : e.timestamp} for e in events]
    }

    

