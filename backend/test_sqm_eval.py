from app.services.sqm_service import generate_query_with_repair


test_alerts = [
    {
        "username": "admin",
        "source_ip": "10.0.0.5",
        "event_type": "failed_login"
    },
    {
        "username": "user1",
        "source_ip": "10.0.0.8",
        "event_type": "credential_access"
    },
    {
        "username": "user2",
        "source_ip": "10.0.0.12",
        "event_type": "lateral_movement"
    },
    {
        "username": "admin",
        "source_ip": "10.0.0.15",
        "event_type": "data_exfiltration"
    }
]


first_try_success = 0
final_success = 0

for alert in test_alerts:

    result = generate_query_with_repair(alert)

    if result["repair_attempts"] == 0 and result["is_valid"]:
        first_try_success += 1

    if result["is_valid"]:
        final_success += 1


total = len(test_alerts)

print(
    f"First-try executable rate: "
    f"{first_try_success}/{total} "
    f"({first_try_success / total * 100:.1f}%)"
)

print(
    f"Final executable rate: "
    f"{final_success}/{total} "
    f"({final_success / total * 100:.1f}%)"
)