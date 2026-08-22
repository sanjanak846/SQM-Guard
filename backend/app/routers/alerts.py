from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Alert

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.post("/ingest")
def ingest_alert(log_data: dict, db: Session = Depends(get_db)):
    new_alert = Alert(raw_fields=log_data)
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return {"id": new_alert.id, "status": new_alert.status}

@router.get("/{alert_id}")
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        return {"error": "Alert not found"}
    return {
        "id": alert.id,
        "timestamp": alert.timestamp,
        "raw_fields": alert.raw_fields,
        "status": alert.status
    }