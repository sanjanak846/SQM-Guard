import sys
import json

sys.path.append("..")

from app.services.sanitizer import sanitize_log_entry


def run_injection_eval(test_cases_path: str):

    with open(test_cases_path, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    total = len(test_cases)
    caught = 0
    false_positives = 0

    results = []

    for case in test_cases:

        # Build log entry using the actual dataset structure
        log_entry = {
            case["field"]: case["value"]
        }

        result = sanitize_log_entry(log_entry)

        was_caught = result["is_suspicious"]

        expected_malicious = (
            case.get("expected", "").lower() == "malicious"
        )

        if expected_malicious and was_caught:
            caught += 1

        if not expected_malicious and was_caught:
            false_positives += 1

        results.append({
            "case_id": case.get("id"),
            "field": case.get("field"),
            "expected": case.get("expected"),
            "caught": was_caught
        })

    malicious_count = sum(
        1
        for case in test_cases
        if case.get("expected", "").lower() == "malicious"
    )

    catch_rate = (
        round((caught / malicious_count) * 100, 2)
        if malicious_count
        else 0
    )

    print("\nInjection Defense Results")
    print("============================")
    print(f"Total test cases: {total}")
    print(
        f"Malicious cases: {malicious_count}"
    )
    print(
        f"Caught: {caught}/{malicious_count} "
        f"({catch_rate}%)"
    )
    print(
        f"False positives: {false_positives}"
    )

    print("\nDetailed Results")
    print("============================")

    for item in results:
        print(
            f"Case {item['case_id']}: "
            f"expected={item['expected']}, "
            f"caught={item['caught']}"
        )

    return results, catch_rate, false_positives


if __name__ == "__main__":

    run_injection_eval(
        "../../datasets/injection_test_cases.json"
    )