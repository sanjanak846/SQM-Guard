from app.services.llm_client import query_llm

result = query_llm(
    "Summarize this security alert in one sentence: "
    "failed login from IP 192.168.1.10, "
    "username admin, 5 attempts in 2 minutes"
)

print(result)