import re
from urllib.parse import unquote
SUSPICIOUS_PATTERNS = [
    r"ign[o0]re\s+(previous|prev[i1]0?us|above|all)?\s*[\s+]*(instructions?|instruct[i1]0?ns?|everything|rules)?",
    r"forget\s+(all|previous|any)?\s*(security\s+)?(rules|instructions)",
    r"disregard\s+(the|any|all|prior)?\s*(prior|previous)?\s*(rules|instructions)",
    r"you are now",
    r"act as (a|an)",
    r"system prompt",
    r"mark (this|it) as (benign|safe|low.?risk)",
    r"approve this (alert|log|entry)",
    r"do not (flag|alert|report)",
    r"</?(system|instruction|prompt)>",
    r"new instructions?:",
    r"system\s+override\s*:",  # only flag "override" when paired with "system" + colon (attack-style), not standalone
]


def is_suspicious(text: str) -> bool:
    if not isinstance(text, str):
        return False
    text_decoded = unquote(text)  # converts %20, +, etc. back to normal characters
    text_lower = text_decoded.lower().replace("+", " ")
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False

def sanitize_field(field_name: str, value: str) -> dict:
    flagged = is_suspicious(value)
    if flagged:
        cleaned_value = "[REDACTED - SUSPICIOUS CONTENT REMOVED]"
    else:
        cleaned_value = value
    return {
        "field_name": field_name,
        "original_value": value,
        "cleaned_value": cleaned_value,
        "flagged": flagged
    }

def sanitize_log_entry(log_entry: dict) -> dict:
    cleaned_entry = {}
    flags = []

    for field_name, value in log_entry.items():
        result = sanitize_field(field_name, value)
        cleaned_entry[field_name] = result["cleaned_value"]
        if result["flagged"]:
            flags.append({
                "field_name": field_name,
                "original_value": result["original_value"]
            })

    return {
        "cleaned_log": cleaned_entry,
        "injection_flags": flags,
        "is_suspicious": len(flags) > 0
    }