import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def query_llm(prompt: str, model: str = "llama3.1:8b") -> dict:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()
        result = response.json()

        return {
            "response": result.get("response", ""),
            "success": True
        }

    except Exception as e:
        return {
            "response": "",
            "success": False,
            "error": str(e)
        }