from app.services.rag_service import load_attack_data, retrieve_technique

load_attack_data("../datasets/enterprise-attack 1/enterprise-attack.json")

results = retrieve_technique("data exfiltration")

for r in results:
    print(r["technique_name"], "-", r["description"])