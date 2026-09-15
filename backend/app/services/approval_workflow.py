
VALID_TRANSITIONS = {
    "pending": ["analyst_review"],
    "anomalous": ["analyst_review", "approved", "rejected"],
    "reviewed": ["analyst_review", "approved", "rejected"],
    "analyst_review": ["approved", "rejected"],
    "approved": ["closed"],
    "rejected": ["closed"],
}

def is_valid_transition(current_status: str, new_status: str) -> bool:
    allowed = VALID_TRANSITIONS.get(current_status, [])
    return new_status in allowed