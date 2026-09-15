def calculate_risk_score(anomaly_result: dict, sanitize_result: dict, query_result: dict) -> dict:
    base_score = anomaly_result.get("risk_score", 0)

    injection_boost = 25 if sanitize_result.get("is_suspicious") else 0
    repair_penalty = query_result.get("repair_attempts", 0) * 5

    final_score = min(100, base_score + injection_boost - repair_penalty)
    final_score = max(0, final_score)

    return {
        "final_risk_score": round(final_score, 2),
        "contributing_factors": {
            "anomaly_score": base_score,
            "injection_detected": sanitize_result.get("is_suspicious", False),
            "query_repair_attempts": query_result.get("repair_attempts", 0)
        }
    }