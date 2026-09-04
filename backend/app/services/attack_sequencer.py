KILL_CHAIN_ORDER = [
    "reconnaissance",
    "initial-access",
    "execution",
    "persistence",
    "privilege-escalation",
    "lateral-movement",
    "collection",
    "exfiltration",
    "impact"
]

def infer_tactic(alert: dict) -> str:
    event_type = alert.get("raw_fields", {}).get("event_type", "").lower()

    if "login" in event_type or "auth" in event_type:
        return "initial-access"
    elif "scan" in event_type or "probe" in event_type:
        return "reconnaissance"
    elif "lateral" in event_type or "remote" in event_type:
        return "lateral-movement"
    elif "exfil" in event_type or "transfer" in event_type:
        return "exfiltration"
    else:
        return "execution"

def is_progressive_sequence(tactics: list) -> bool:
    positions = [KILL_CHAIN_ORDER.index(t) for t in tactics if t in KILL_CHAIN_ORDER]
    return positions == sorted(positions) and len(set(positions)) > 1