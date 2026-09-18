import json
from pathlib import Path

from app.services.query_validator import validate_query
from app.services.llm_client import query_llm
from app.services.rag_service import retrieve_technique


def load_reference_queries():
    base_dir = Path(__file__).resolve().parents[2]
    reference_file = base_dir / "data" / "reference_queries.json"

    with open(reference_file, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_query(alert: dict) -> dict:
    reference_queries = load_reference_queries()

    examples_text = "\n".join(
        [
            f"- {q['description']}: {q['query']}"
            for q in reference_queries[:5]
        ]
    )

    attack_context = retrieve_technique(
        alert.get("event_type", "suspicious activity"),
        top_k=2
    )

    context_text = "\n".join(
        [
            f"{a['technique_name']}: {a['description']}"
            for a in attack_context
        ]
    )

    prompt = f"""
You are a KQL query generator for Microsoft Sentinel.

Generate ONLY a valid KQL query.
Do not provide explanations.

Alert:
{json.dumps(alert)}

Reference query examples:
{examples_text}

Relevant MITRE ATT&CK context:
{context_text}

Output only the KQL query.
"""

    result = query_llm(prompt)

    return {
        "generated_query": result["response"].strip(),
        "success": result["success"]
    }

def generate_query_with_repair(alert: dict, max_retries: int = 1) -> dict:
    result = generate_query(alert)

    validation = validate_query(result["generated_query"])

    attempts = 0

    while not validation["is_valid"] and attempts < max_retries:
        attempts += 1

        repair_prompt = f"""
The following KQL query has errors:

{validation["errors"]}

Original query:
{result["generated_query"]}

Correct the query.

Return ONLY the corrected KQL query.
Do not provide explanations.
"""

        repair_result = query_llm(repair_prompt)

        result["generated_query"] = repair_result["response"].strip()

        validation = validate_query(
            result["generated_query"]
        )

    return {
        "final_query": result["generated_query"],
        "is_valid": validation["is_valid"],
        "remaining_errors": validation["errors"],
        "repair_attempts": attempts
    }