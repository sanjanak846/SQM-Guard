from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Alert
from app.services.anomaly_scorer import score_alert
from app.services.sqm_service import generate_query_with_repair

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

@router.post("/{alert_id}/detect")
def detect_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        return {"error": "Alert not found"}

    result = score_alert(alert.raw_fields)

    alert.status = "anomalous" if result["is_anomaly"] else "reviewed"

    db.commit()

    return {
        "id": alert.id,
        "is_anomaly": result["is_anomaly"],
        "risk_score": result["risk_score"],
        "status": alert.status
    }

@router.post("/{alert_id}/generate-query")
def generate_query_endpoint(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        return {"error": "Alert not found"}

    result = generate_query_with_repair(alert.raw_fields)

    return {
        "id": alert.id,
        **result
    }