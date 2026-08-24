import re

SUSPICIOUS_PATTERNS = [
    r"ignore (previous|above|all)?[\s+]*(instructions|everything|rules)?",
    r"forget (all|previous|any) (security )?(rules|instructions)",
    r"disregard (the|any) (prior|previous) (rules|instructions)",
    r"you are now",
    r"act as (a|an)",
    r"system prompt",
    r"mark (this|it) as (benign|safe|low.?risk)",
    r"approve this (alert|log|entry)",
    r"do not (flag|alert|report)",
    r"</?(system|instruction|prompt)>",
    r"new instructions?:",
    r"override",
    r"system override",
]

import re
from urllib.parse import unquote

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