from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    raw_fields = Column(JSON)
    status = Column(String, default="pending")


class ApprovalLog(Base):
    __tablename__ = "approval_log"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer)
    from_status = Column(String)
    to_status = Column(String)
    actor = Column(String, default="analyst")
    timestamp = Column(DateTime, default=datetime.utcnow)
    comment = Column(String, nullable=True)

class Resolution(Base):
    __tablename__ = "resolutions"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer)
    risk_score = Column(Integer)
    resolution_category = Column(String)
    justification = Column(String)