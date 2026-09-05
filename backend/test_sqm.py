from app.services.sqm_service import generate_query_with_repair


alert = {
    "username": "admin",
    "source_ip": "192.168.1.10",
    "event_type": "failed_login",
    "description": "Five failed login attempts in two minutes"
}


result = generate_query_with_repair(alert)

print("\nSQM RESULT")
print("====================")
print("Final Query:")
print(result["final_query"])

print("\nValid:")
print(result["is_valid"])

print("\nErrors:")
print(result["remaining_errors"])

print("\nRepair Attempts:")
print(result["repair_attempts"])