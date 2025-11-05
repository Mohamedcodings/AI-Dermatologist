from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.dermatologist import analyze_skin

router = APIRouter()

@router.post("/skin/analyze")
async def analyze_skin_endpoint(
    file: UploadFile = File(...)
):
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(status_code=400, detail="Only JPEG or PNG allowed")

    image_bytes = await file.read()
    result = await analyze_skin(image_bytes)
    return result
