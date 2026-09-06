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


def generate_resolution(
    alert: dict,
    risk_data: dict,
    generated_query: str
) -> dict:

    prompt = f"""
You are a SOC analyst assistant.

Based on the following security alert information, recommend the most appropriate resolution.

Alert details:
{json.dumps(alert)}

Risk score:
{risk_data['final_risk_score']}

Contributing factors:
{json.dumps(risk_data['contributing_factors'])}

Investigation query:
{generated_query}

Choose ONE resolution category from this list:

{RESOLUTION_CATEGORIES}

Respond ONLY in this JSON format:

{{
    "category": "chosen category",
    "justification": "2-3 sentence explanation"
}}

Do not provide any text outside the JSON.
"""

    result = query_llm(prompt)

    if not result["success"]:
        return {
            "category": "Requires Further Investigation",
            "justification": "The language model could not be reached, so manual investigation is required."
        }

    try:
        parsed = json.loads(result["response"])

        if parsed.get("category") not in RESOLUTION_CATEGORIES:
            return {
                "category": "Requires Further Investigation",
                "justification": "The model returned an unsupported resolution category."
            }

        return {
            "category": parsed["category"],
            "justification": parsed.get(
                "justification",
                "Resolution recommended based on the available alert evidence."
            )
        }

    except json.JSONDecodeError:
        return {
            "category": "Requires Further Investigation",
            "justification": "The model output could not be parsed as JSON, so manual investigation is required."
        }