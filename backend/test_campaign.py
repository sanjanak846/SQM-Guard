from app.services.entity_graph import detect_campaigns

test_alerts = [
    {"id": 1, "raw_fields": {"username": "admin", "source_ip": "10.0.0.5", "event_type": "port scan"}},
    {"id": 2, "raw_fields": {"username": "admin", "source_ip": "10.0.0.5", "event_type": "failed login"}},
    {"id": 3, "raw_fields": {"username": "admin", "source_ip": "10.0.0.5", "event_type": "lateral movement to server2"}},
    {"id": 4, "raw_fields": {"username": "guest", "source_ip": "10.0.0.99", "event_type": "normal login"}},
]

campaigns = detect_campaigns(test_alerts)
print(f"Found {len(campaigns)} campaign(s):")
for c in campaigns:
    print(c)