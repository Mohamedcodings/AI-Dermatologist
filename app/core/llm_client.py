import os
import httpx

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "dummy")

API_URL = "https://api.mistral.ai/v1/chat/completions"

async def ask_llm(prompt: str) -> str:
    # allow app to run without real key
    if MISTRAL_API_KEY == "dummy":
        return "This could be a mild skin issue. Keep the area clean, avoid scratching, and monitor for changes. This is not a diagnosis."

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
    }
    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(API_URL, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]
