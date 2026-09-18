import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.entity_graph import detect_campaigns


def run_campaign_eval():

    # Scenario 1: Multi-stage attack
    scenario_1 = [
        {
            "id": 1,
            "raw_fields": {
                "username": "admin",
                "source_ip": "10.0.0.5",
                "event_type": "port scan"
            }
        },
        {
            "id": 2,
            "raw_fields": {
                "username": "admin",
                "source_ip": "10.0.0.5",
                "event_type": "failed login"
            }
        },
        {
            "id": 3,
            "raw_fields": {
                "username": "admin",
                "source_ip": "10.0.0.5",
                "event_type": "lateral movement"
            }
        }
    ]

    # Scenario 2: Unrelated alerts
    scenario_2 = [
        {
            "id": 4,
            "raw_fields": {
                "username": "guest",
                "source_ip": "10.0.0.99",
                "event_type": "normal login"
            }
        },
        {
            "id": 5,
            "raw_fields": {
                "username": "bob",
                "source_ip": "10.0.0.44",
                "event_type": "file access"
            }
        }
    ]

    combined = scenario_1 + scenario_2

    campaigns = detect_campaigns(combined)

    correctly_grouped = any(
        set(c["alert_ids"]) == {1, 2, 3}
        for c in campaigns
    )

    correctly_excluded = not any(
        4 in c["alert_ids"] or 5 in c["alert_ids"]
        for c in campaigns
    )

    print("\n")
    print("======================================")
    print("CAMPAIGN CORRELATION RESULTS")
    print("======================================")

    print(
        "Multi-stage attack correctly grouped:",
        correctly_grouped
    )

    print(
        "Unrelated alerts correctly excluded:",
        correctly_excluded
    )

    print(
        "Total campaigns detected:",
        len(campaigns)
    )


if __name__ == "__main__":
    run_campaign_eval()