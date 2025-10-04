from sqlalchemy import Column, Integer, String, Boolean,DateTime,ForeignKey,func
from database.db import Base
from sqlalchemy.orm import relationship
import uuid

class Credits(Base):
    __tablename__ = "credits"
    id = Column(String,primary_key = True,index  = True)
    project_name = Column(String, nullable = False)
    registry = Column(String, nullable = False)
    vintage = Column(Integer, nullable = False)
    quantity = Column(Integer, nullable = False)
    serial_number = Column(String, nullable = False)

    events = relationship("Events",back_populates = "record",cascade="all, delete-orphan")



class Events(Base):

    __tablename__ = "events_record"

    id = Column(String, primary_key = True, default=lambda: str(uuid.uuid4()))
    record_id = Column(String, ForeignKey("credits.id"),nullable = False)

    event_type = Column(String, nullable = False)
    
    timestamp = Column(DateTime(timezone = True),server_default = func.now())

    record = relationship("Credits",back_populates = "events")