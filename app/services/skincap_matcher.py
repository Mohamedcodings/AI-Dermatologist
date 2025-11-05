# app/services/skincap_matcher.py
import re
from typing import Dict, List, Any
from app.services.skincap_loader import load_skincap

def tokenize(text: str) -> List[str]:
    text = text.lower()
    return re.findall(r"[a-z]+", text)

def match_description_in_skincap(description: str, top_k: int = 3) -> List[Dict[str, Any]]:
    skincap_data = load_skincap()
    desc_tokens = set(tokenize(description))

    scored: List[Dict[str, Any]] = []
    for row in skincap_data:
        caption = row.get("caption", "") or ""
        label = row.get("label", "") or ""
        cap_tokens = set(tokenize(caption))
        score = len(desc_tokens & cap_tokens)
        if score > 0:
            scored.append({
                "score": score,
                "caption": caption,
                "label": label
            })

    # sort by score desc
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
