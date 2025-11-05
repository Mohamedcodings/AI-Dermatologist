from fastapi import FastAPI
from app.api import skin
from pathlib import Path
import logging

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass  # python-dotenv not installed, skip

app = FastAPI(title="Skin AI Dermatologist")

app.include_router(skin.router, prefix="/api")

logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Load the SkinCAP dataset on startup."""
    try:
        from app.services.skincap_loader import load_skincap
        logger.info("Loading SkinCAP dataset on startup...")
        data = load_skincap()
        logger.info(f"Successfully loaded {len(data)} items from SkinCAP dataset.")
    except Exception as e:
        logger.warning(f"Could not load SkinCAP dataset on startup: {e}")
        logger.info("The app will use fallback data or try to load on first request.")

@app.get("/health")
def health():
    return {"status": "ok"}
