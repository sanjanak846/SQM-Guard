from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    raw_fields = Column(JSON)
    status = Column(String, default="pending")