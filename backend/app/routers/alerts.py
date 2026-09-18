from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import logging

from app.database import get_db
<<<<<<< HEAD
from app.models import Alert, Resolution
=======
from app.models import Alert, Resolution, ApprovalLog
>>>>>>> 7c13b76 (Phase 13: finalized database schema and logging)
from app.services.sanitizer import sanitize_log_entry
from app.services.anomaly_scorer import score_alert
from app.services.sqm_service import generate_query_with_repair
from app.services.risk_scoring import calculate_risk_score
from app.services.resolution_service import generate_resolution
<<<<<<< HEAD
from app.models import ApprovalLog
=======
>>>>>>> 7c13b76 (Phase 13: finalized database schema and logging)
from app.services.approval_workflow import is_valid_transition


router = APIRouter(prefix="/alerts", tags=["alerts"])

<<<<<<< HEAD
@router.get("/")
def list_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).all()
    return [
        {
            "id": a.id,
            "timestamp": a.timestamp,
            "status": a.status,
            "risk_score": getattr(a, "risk_score", None),
            "raw_fields": a.raw_fields,
        }
        for a in alerts
    ]
=======
logger = logging.getLogger(__name__)


# --------------------------------------------------
# INGEST ALERT
# --------------------------------------------------
>>>>>>> 7c13b76 (Phase 13: finalized database schema and logging)

@router.post("/ingest")
def ingest_alert(log_data: dict, db: Session = Depends(get_db)):

    new_alert = Alert(raw_fields=log_data)

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    logger.info(f"Alert {new_alert.id} ingested")

    return {
        "id": new_alert.id,
        "status": new_alert.status
    }


# --------------------------------------------------
# GET ALERT
# --------------------------------------------------

@router.get("/{alert_id}")
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):

    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        logger.warning(f"Alert {alert_id} not found")
        return {"error": "Alert not found"}

    return {
        "id": alert.id,
        "timestamp": alert.timestamp,
        "raw_fields": alert.raw_fields,
        "status": alert.status
    }


# --------------------------------------------------
# SANITIZE ALERT
# --------------------------------------------------

@router.post("/{alert_id}/sanitize")
def sanitize_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):

    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        return {"error": "Alert not found"}

    result = sanitize_log_entry(
        alert.raw_fields
    )

    return {
        "id": alert.id,
        "cleaned_log": result["cleaned_log"],
        "injection_flags": result["injection_flags"],
        "is_suspicious": result["is_suspicious"]
    }


# --------------------------------------------------
# ANOMALY DETECTION
# --------------------------------------------------

@router.post("/{alert_id}/detect")
def detect_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):

    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        return {"error": "Alert not found"}

    result = score_alert(
        alert.raw_fields
    )

    alert.status = (
        "anomalous"
        if result["is_anomaly"]
        else "reviewed"
    )

    db.commit()

    logger.info(
        f"Alert {alert.id} anomaly detection completed"
    )

    return {
        "id": alert.id,
        "is_anomaly": result["is_anomaly"],
        "risk_score": result["risk_score"],
        "status": alert.status
    }


# --------------------------------------------------
# GENERATE INVESTIGATION QUERY
# --------------------------------------------------

@router.post("/{alert_id}/generate-query")
def generate_query_endpoint(
    alert_id: int,
    db: Session = Depends(get_db)
):

    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        return {"error": "Alert not found"}

    result = generate_query_with_repair(
        alert.raw_fields
    )

    return {
        "id": alert.id,
        **result
    }


# --------------------------------------------------
# PROCESS ALERT
# --------------------------------------------------

@router.post("/{alert_id}/process")
def process_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):

    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        return {"error": "Alert not found"}

    sanitize_result = sanitize_log_entry(
        alert.raw_fields
    )

    detection_result = score_alert(
        sanitize_result["cleaned_log"]
    )

    alert.status = (
        "anomalous"
        if detection_result["is_anomaly"]
        else "reviewed"
    )

    db.commit()

    logger.info(
        f"Alert {alert.id} processed"
    )

    return {
        "id": alert.id,
        "injection_flags": sanitize_result["injection_flags"],
        "is_suspicious_input": sanitize_result["is_suspicious"],
        "is_anomaly": detection_result["is_anomaly"],
        "risk_score": detection_result["risk_score"],
        "status": alert.status
    }


# --------------------------------------------------
# APPROVAL LOG HELPER
# --------------------------------------------------

def log_transition(
    db: Session,
    alert_id: int,
    from_status: str,
    to_status: str,
    comment: str = None
):

    log_entry = ApprovalLog(
        alert_id=alert_id,
        from_status=from_status,
        to_status=to_status,
        comment=comment
    )

    db.add(log_entry)
    db.commit()


# --------------------------------------------------
# SUBMIT FOR REVIEW
# --------------------------------------------------

@router.post("/{alert_id}/submit-for-review")
def submit_for_review(
    alert_id: int,
    db: Session = Depends(get_db)
):

    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        return {"error": "Alert not found"}

    if not is_valid_transition(
        alert.status,
        "analyst_review"
    ):
        return {
            "error":
            f"Cannot submit alert with status "
            f"'{alert.status}' for review"
        }

    old_status = alert.status

    alert.status = "analyst_review"

    db.commit()

    log_transition(
        db,
        alert_id,
        old_status,
        "analyst_review"
    )

    logger.info(
        f"Alert {alert.id} submitted for review"
    )

    return {
        "id": alert.id,
        "status": alert.status
    }


# --------------------------------------------------
# APPROVE ALERT
# --------------------------------------------------

@router.post("/{alert_id}/approve")
def approve_alert(
    alert_id: int,
    comment: str = None,
    db: Session = Depends(get_db)
):

    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        return {"error": "Alert not found"}

    if not is_valid_transition(
        alert.status,
        "approved"
    ):
        return {
            "error":
            f"Cannot approve an alert with status "
            f"'{alert.status}'"
        }

    old_status = alert.status

    alert.status = "approved"

    db.commit()

    log_transition(
        db,
        alert_id,
        old_status,
        "approved",
        comment
    )

    logger.info(
        f"Alert {alert.id} approved"
    )

    return {
        "id": alert.id,
        "status": alert.status
    }


# --------------------------------------------------
# REJECT ALERT
# --------------------------------------------------

@router.post("/{alert_id}/reject")
def reject_alert(
    alert_id: int,
    comment: str = None,
    db: Session = Depends(get_db)
):

    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        return {"error": "Alert not found"}

    if not is_valid_transition(
        alert.status,
        "rejected"
    ):
        return {
            "error":
            f"Cannot reject an alert with status "
            f"'{alert.status}'"
        }

    old_status = alert.status

    alert.status = "rejected"

    db.commit()

    log_transition(
        db,
        alert_id,
        old_status,
        "rejected",
        comment
    )

    logger.info(
        f"Alert {alert.id} rejected"
    )

    return {
        "id": alert.id,
        "status": alert.status
    }


# --------------------------------------------------
# ALERT HISTORY
# --------------------------------------------------

@router.get("/{alert_id}/history")
def get_alert_history(
    alert_id: int,
    db: Session = Depends(get_db)
):

    logs = db.query(ApprovalLog).filter(
        ApprovalLog.alert_id == alert_id
    ).all()

    return [
        {
            "from_status": l.from_status,
            "to_status": l.to_status,
            "actor": l.actor,
            "timestamp": l.timestamp,
            "comment": l.comment
        }
        for l in logs
    ]


# --------------------------------------------------
# RESOLVE ALERT
# --------------------------------------------------

<<<<<<< HEAD
=======
@router.post("/{alert_id}/resolve")
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):

    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()
>>>>>>> 7c13b76 (Phase 13: finalized database schema and logging)

@router.post("/{alert_id}/resolve")
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        logger.warning(
            f"Resolve requested for missing alert {alert_id}"
        )
        return {"error": "Alert not found"}

<<<<<<< HEAD
    sanitize_result = sanitize_log_entry(alert.raw_fields)
    anomaly_result = score_alert(sanitize_result["cleaned_log"])
    query_result = generate_query_with_repair(sanitize_result["cleaned_log"])
=======
    # Step 1: Sanitize the alert
    sanitize_result = sanitize_log_entry(
        alert.raw_fields
    )
>>>>>>> 7c13b76 (Phase 13: finalized database schema and logging)

    risk_data = calculate_risk_score(anomaly_result, sanitize_result, query_result)
    resolution = generate_resolution(alert.raw_fields, risk_data, query_result.get("final_query", ""))

    alert.risk_score = int(risk_data["final_risk_score"])
    alert.status = "anomalous" if anomaly_result["is_anomaly"] else "reviewed"
    db.commit()

<<<<<<< HEAD
    resolution_entry = Resolution(
        alert_id=alert_id,
        risk_score=risk_data["final_risk_score"],
=======
    # Step 4: Calculate final risk score
    risk_data = calculate_risk_score(
        anomaly_result,
        sanitize_result,
        query_result
    )

    # Step 5: Generate resolution recommendation
    resolution = generate_resolution(
        alert.raw_fields,
        risk_data,
        query_result["final_query"]
    )

    # Step 6: Save resolution
    resolution_entry = Resolution(
        alert_id=alert_id,
        risk_score=round(
            risk_data["final_risk_score"]
        ),
>>>>>>> 7c13b76 (Phase 13: finalized database schema and logging)
        resolution_category=resolution["category"],
        justification=resolution["justification"]
    )
    db.add(resolution_entry)
    db.commit()

    logger.info(
        f"Alert {alert.id} resolved"
    )

    return {
        "id": alert.id,
        "risk_score": risk_data["final_risk_score"],
        "contributing_factors": risk_data["contributing_factors"],
        "resolution": resolution
    }