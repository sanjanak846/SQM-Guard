from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Alert
from app.services.entity_graph import detect_campaigns

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

@router.get("/")
def get_campaigns(db: Session = Depends(get_db)):
    all_alerts = db.query(Alert).all()
    alert_dicts = [{"id": a.id, "raw_fields": a.raw_fields} for a in all_alerts]
    campaigns = detect_campaigns(alert_dicts)
    return campaigns