from app.services.entity_graph import detect_campaigns

# ---------------------------------------------------------
# Test 1: A genuine multi-stage campaign (same user/IP,
# tactics in proper kill-chain order) + one unrelated alert
# ---------------------------------------------------------
test_alerts_1 = [
    {"id": 1, "raw_fields": {"username": "admin", "source_ip": "10.0.0.5", "event_type": "port scan"}},
    {"id": 2, "raw_fields": {"username": "admin", "source_ip": "10.0.0.5", "event_type": "failed login"}},
    {"id": 3, "raw_fields": {"username": "admin", "source_ip": "10.0.0.5", "event_type": "lateral movement to server2"}},
    {"id": 4, "raw_fields": {"username": "guest", "source_ip": "10.0.0.99", "event_type": "normal login"}},
]

campaigns_1 = detect_campaigns(test_alerts_1)
print(f"Test 1 — Found {len(campaigns_1)} campaign(s):")
for c in campaigns_1:
    print(c)

# ---------------------------------------------------------
# Test 2: Trickier cases
# - Alerts 5 & 6 share an IP, but tactics are OUT of
#   kill-chain order (lateral movement before recon) —
#   should NOT be grouped as a progressive campaign
# - Alerts 7 & 8 share no entities at all — should
#   definitely not be grouped
# ---------------------------------------------------------
test_alerts_2 = [
    {"id": 5, "raw_fields": {"username": "bob", "source_ip": "20.0.0.5", "event_type": "lateral movement to server3"}},
    {"id": 6, "raw_fields": {"username": "bob", "source_ip": "20.0.0.5", "event_type": "port scan"}},
    {"id": 7, "raw_fields": {"username": "carol", "source_ip": "30.0.0.1", "event_type": "normal login"}},
    {"id": 8, "raw_fields": {"username": "dave", "source_ip": "40.0.0.2", "event_type": "file access"}},
]

campaigns_2 = detect_campaigns(test_alerts_2)
print(f"\nTest 2 — Found {len(campaigns_2)} campaign(s):")
for c in campaigns_2:
    print(c)