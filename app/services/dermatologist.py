from app.services.vision_client import describe_image_with_mistral
from app.services.skincap_matcher import match_description_in_skincap

DISCL = "This is not a medical diagnosis. Please consult a healthcare professional."

async def analyze_skin(image_bytes: bytes) -> dict:
    # 1) get description from Mistral vision
    desc = await describe_image_with_mistral(image_bytes)

    # 2) match against SkinCAP dataset
    matches = match_description_in_skincap(desc, top_k=3)

    # pick the top match if exists
    if matches:
        best = matches[0]
        predicted = best["label"] or "Unknown (no label in dataset)"
        score = best["score"]
        example_caption = best["caption"]
    else:
        predicted = "Unknown"
        score = 0
        example_caption = ""

    return {
        "vision_description": desc,
        "predicted_condition": predicted,
        "match_score": score,
        "example_caption": example_caption,
        "top_matches": matches,
        "disclaimer": DISCL
    }
