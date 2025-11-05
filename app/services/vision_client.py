import os
import httpx
from pathlib import Path

# Try to load .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass  # python-dotenv not installed, skip

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "dummy")
API_URL = os.getenv("MISTRAL_API_URL", "https://api.mistral.ai/v1/chat/completions")
VISION_MODEL = os.getenv("MISTRAL_VISION_MODEL", "pixtral-large-latest")

async def describe_image_with_mistral(image_bytes: bytes) -> str:
    """
    Takes raw image bytes and calls Mistral's multimodal API to get a text description.
    Returns only the text description of the visible skin lesion.
    """
    # Reload env to ensure we have the latest key
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent.parent.parent / ".env"
        load_dotenv(env_path, override=True)
    except ImportError:
        pass
    
    # Get key after reloading
    api_key = os.getenv("MISTRAL_API_KEY", MISTRAL_API_KEY)
    
    if api_key == "dummy" or not api_key:
        print("WARNING: MISTRAL_API_KEY is 'dummy' or empty, using mock response")
        return "Mock: single red scaly patch on the cheek."

    print(f"Using Mistral API key (length: {len(api_key)})")
    
    # Prepare the request
    headers = {"Authorization": f"Bearer {api_key}"}
    
    import base64
    
    # Convert image bytes to base64
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # Mistral's vision API format
    payload = {
        "model": VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe the visible skin lesion: color, raised/flat, single/multiple, redness. Do NOT diagnose."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ]
    }
    
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            print(f"Calling Mistral API: {API_URL}")
            resp = await client.post(API_URL, headers=headers, json=payload)
            resp.raise_for_status()
            body = resp.json()
            result = body["choices"][0]["message"]["content"]
            print(f"Mistral API response received (length: {len(result)})")
            return result
    except httpx.HTTPStatusError as e:
        print(f"Mistral API error: {e.response.status_code} - {e.response.text}")
        raise RuntimeError(f"Mistral API error: {e.response.status_code} - {e.response.text}") from e
    except Exception as e:
        print(f"Error calling Mistral API: {e}")
        raise RuntimeError(f"Error calling Mistral API: {e}") from e

