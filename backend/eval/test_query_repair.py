import sys

sys.path.append("..")

from app.services.sqm_service import generate_query_with_repair


test_alerts = [
    {
        "username": "admin",
        "source_ip": "10.0.0.5",
        "event_type": "failed_login",
        "description": "Multiple failed login attempts"
    },
    {
        "username": "guest",
        "source_ip": "10.0.0.12",
        "event_type": "port_scan",
        "description": "Suspicious port scanning activity"
    },
    {
        "username": "svc_account",
        "source_ip": "192.168.1.20",
        "event_type": "lateral movement",
        "description": "Possible lateral movement"
    },
    {
        "username": "admin",
        "source_ip": "192.168.1.10",
        "event_type": "credential access",
        "description": "Possible credential access activity"
    },
    {
        "username": "user1",
        "source_ip": "10.0.0.15",
        "event_type": "network_activity",
        "description": "Unusual network connection"
    },
    {
        "username": "user2",
        "source_ip": "10.0.0.20",
        "event_type": "account_activity",
        "description": "Suspicious account activity"
    },
    {
        "username": "admin",
        "source_ip": "10.0.0.25",
        "event_type": "process_activity",
        "description": "Suspicious process activity"
    },
    {
        "username": "guest",
        "source_ip": "10.0.0.30",
        "event_type": "failed_login",
        "description": "Repeated authentication failures"
    },
    {
        "username": "analyst",
        "source_ip": "192.168.1.30",
        "event_type": "login",
        "description": "Successful login"
    },
    {
        "username": "svc_backup",
        "source_ip": "192.168.1.40",
        "event_type": "network_activity",
        "description": "Unexpected network activity"
    },
    {
        "username": "admin",
        "source_ip": "10.0.0.40",
        "event_type": "data_exfiltration",
        "description": "Possible data exfiltration"
    },
    {
        "username": "user3",
        "source_ip": "10.0.0.50",
        "event_type": "account_activity",
        "description": "Unusual account event"
    },
    {
        "username": "user4",
        "source_ip": "10.0.0.60",
        "event_type": "process_activity",
        "description": "Unusual process execution"
    },
    {
        "username": "admin",
        "source_ip": "10.0.0.70",
        "event_type": "failed_login",
        "description": "Failed authentication attempt"
    },
    {
        "username": "service",
        "source_ip": "192.168.1.70",
        "event_type": "lateral movement",
        "description": "Possible remote access activity"
    }
]


def run_query_repair_eval(alerts):

    first_try_success = 0
    final_success = 0
    total_repair_attempts = 0

    for index, alert in enumerate(alerts, start=1):

        print(f"\nTesting alert {index}...")
        print("--------------------------------")

        result = generate_query_with_repair(alert)

        print("Final Query:")
        print(result["final_query"])

        print("Valid:", result["is_valid"])
        print("Repair Attempts:", result["repair_attempts"])

        if result["repair_attempts"] == 0 and result["is_valid"]:
            first_try_success += 1

        if result["is_valid"]:
            final_success += 1

        total_repair_attempts += result["repair_attempts"]

    total = len(alerts)

    first_try_rate = round(
        (first_try_success / total) * 100, 2
    )

    final_rate = round(
        (final_success / total) * 100, 2
    )

    improvement = round(
        final_rate - first_try_rate, 2
    )

    print("\n")
    print("======================================")
    print("QUERY GENERATION & REPAIR RESULTS")
    print("======================================")
    print(f"Total alerts: {total}")
    print(
        f"First-try executable rate: "
        f"{first_try_rate}%"
    )
    print(
        f"Final executable rate: "
        f"{final_rate}%"
    )
    print(
        f"Improvement from repair: "
        f"{improvement} percentage points"
    )
    print(
        f"Total repair attempts: "
        f"{total_repair_attempts}"
    )


if __name__ == "__main__":
    run_query_repair_eval(test_alerts)