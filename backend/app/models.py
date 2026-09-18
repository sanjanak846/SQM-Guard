

from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean

from datetime import datetime
from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    raw_fields = Column(JSON)

=======
    status = Column(String, default="pending", index=True)
    risk_score = Column(Integer, nullable=True, index=True)



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
    risk_score = Column(Float)
    resolution_category = Column(String)
    justification = Column(String)

class InjectionFlag(Base):
    __tablename__ = "injection_flags"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, index=True)
    field_name = Column(String)
    original_value = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class GeneratedQuery(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, index=True)
    generated_query = Column(String)
    is_valid = Column(Boolean)
    repair_attempts = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)