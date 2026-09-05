def validate_query(query: str) -> dict:
    errors = []

    KNOWN_TABLE_NAMES = [
        "SigninLogs",
        "SecurityEvent",
        "AuditLogs",
        "AzureActivity"
    ]

    if not query or len(query.strip()) < 5:
        errors.append("Query is empty or too short")

    if "|" not in query:
        errors.append(
            "Missing pipe operator '|' — not valid KQL structure"
        )

    if not any(table in query for table in KNOWN_TABLE_NAMES):
        errors.append(
            f"No recognized table name found. Expected one of: {KNOWN_TABLE_NAMES}"
        )

    if query.count("(") != query.count(")"):
        errors.append("Unbalanced parentheses")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }