from app.services.llm_client import query_llm
import json

RESOLUTION_CATEGORIES = [
    "External Attack - Confirmed",
    "External Attack - Unsuccessful",
    "Insider Threat",
    "False Positive",
    "Policy Violation",
    "Requires Further Investigation",
    "Benign - No Action Needed"
]

def generate_resolution(alert: dict, risk_data: dict, generated_query: str) -> dict:
    prompt = f"""You are a SOC analyst assistant. Based on the following information, recommend a resolution.

Alert details: {json.dumps(alert)}
Risk score: {risk_data['final_risk_score']}
Contributing factors: {json.dumps(risk_data['contributing_factors'])}
Investigation query used: {generated_query}

Choose ONE resolution category from this list: {RESOLUTION_CATEGORIES}

Respond in this exact JSON format:
{{"category": "chosen category", "justification": "2-3 sentence explanation"}}"""

    result = query_llm(prompt)
    try:
        parsed = json.loads(result["response"])
        return parsed
    except:
        return {"category": "Requires Further Investigation", "justification": "Could not parse model output — defaulting to manual review."}