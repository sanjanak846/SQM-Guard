from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Alert
from app.services.sanitizer import sanitize_log_entry
from app.services.anomaly_scorer import score_alert

from app.models import ApprovalLog
from app.services.approval_workflow import is_valid_transition

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

@router.post("/{alert_id}/sanitize")
def sanitize_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        return {"error": "Alert not found"}

    result = sanitize_log_entry(alert.raw_fields)

    return {
        "id": alert.id,
        "cleaned_log": result["cleaned_log"],
        "injection_flags": result["injection_flags"],
        "is_suspicious": result["is_suspicious"]
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

@router.post("/{alert_id}/process")
def process_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        return {"error": "Alert not found"}

    sanitize_result = sanitize_log_entry(alert.raw_fields)
    detection_result = score_alert(sanitize_result["cleaned_log"])

    alert.status = "anomalous" if detection_result["is_anomaly"] else "reviewed"
    db.commit()

    return {
        "id": alert.id,
        "injection_flags": sanitize_result["injection_flags"],
        "is_suspicious_input": sanitize_result["is_suspicious"],
        "is_anomaly": detection_result["is_anomaly"],
        "risk_score": detection_result["risk_score"],
        "status": alert.status
    }

def log_transition(db: Session, alert_id: int, from_status: str, to_status: str, comment: str = None):
    log_entry = ApprovalLog(alert_id=alert_id, from_status=from_status, to_status=to_status, comment=comment)
    db.add(log_entry)
    db.commit()

@router.post("/{alert_id}/submit-for-review")
def submit_for_review(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        return {"error": "Alert not found"}
    if not is_valid_transition(alert.status, "analyst_review"):
        return {"error": f"Cannot submit alert with status '{alert.status}' for review"}
    old_status = alert.status
    alert.status = "analyst_review"
    db.commit()
    log_transition(db, alert_id, old_status, "analyst_review")
    return {"id": alert.id, "status": alert.status}

@router.post("/{alert_id}/approve")
def approve_alert(alert_id: int, comment: str = None, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        return {"error": "Alert not found"}
    if not is_valid_transition(alert.status, "approved"):
        return {"error": f"Cannot approve an alert with status '{alert.status}'"}
    old_status = alert.status
    alert.status = "approved"
    db.commit()
    log_transition(db, alert_id, old_status, "approved", comment)
    return {"id": alert.id, "status": alert.status}

@router.post("/{alert_id}/reject")
def reject_alert(alert_id: int, comment: str = None, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        return {"error": "Alert not found"}
    if not is_valid_transition(alert.status, "rejected"):
        return {"error": f"Cannot reject an alert with status '{alert.status}'"}
    old_status = alert.status
    alert.status = "rejected"
    db.commit()
    log_transition(db, alert_id, old_status, "rejected", comment)
    return {"id": alert.id, "status": alert.status}

@router.get("/{alert_id}/history")
def get_alert_history(alert_id: int, db: Session = Depends(get_db)):
    logs = db.query(ApprovalLog).filter(ApprovalLog.alert_id == alert_id).all()
    return [{"from_status": l.from_status, "to_status": l.to_status, "actor": l.actor, "timestamp": l.timestamp, "comment": l.comment} for l in logs]
