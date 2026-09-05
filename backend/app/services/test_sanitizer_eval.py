import json
from sanitizer import sanitize_field

def evaluate_sanitizer(test_cases_path: str):
    with open(test_cases_path, "r") as f:
        test_cases = json.load(f)

    total = len(test_cases)
    correct = 0
    results = []

    for case in test_cases:
        result = sanitize_field(case["field"], case["value"])
        predicted = "malicious" if result["flagged"] else "safe"
        is_correct = predicted == case["expected"]
        if is_correct:
            correct += 1
        results.append({
            "case_id": case["id"],
            "field": case["field"],
            "expected": case["expected"],
            "predicted": predicted,
            "correct": is_correct
        })
        print(f"Case {case['id']} ({case['field']}): expected={case['expected']}, predicted={predicted}, {'✅' if is_correct else '❌'}")

    accuracy = round((correct / total) * 100, 2)
    print(f"\nSanitizer accuracy: {correct}/{total} correct ({accuracy}%)")
    return results, accuracy

if __name__ == "__main__":
   evaluate_sanitizer("../../../datasets/injection_test_cases.json")