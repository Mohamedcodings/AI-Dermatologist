# app/services/skincap_loader.py
import os
from pathlib import Path
from datasets import load_dataset
from typing import List, Dict

# Try to load .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass  # python-dotenv not installed, skip

# we load once and reuse
_dataset_cache: List[Dict] | None = None

def load_skincap() -> List[Dict]:
    global _dataset_cache
    if _dataset_cache is not None:
        return _dataset_cache

    # Get Hugging Face token from environment (required for gated datasets)
    hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
    
    if not hf_token:
        raise ValueError(
            "HF_TOKEN or HUGGINGFACE_TOKEN environment variable is required. "
            "This dataset is gated and requires authentication. "
            "Set your token: export HF_TOKEN='your-token-here'"
        )

    # Load metadata from CSV file (captions and labels)
    # The CSV file contains all the metadata we need without requiring image access
    try:
        from huggingface_hub import hf_hub_download
        import pandas as pd
        
        print("Downloading SkinCAP metadata CSV file...")
        # Download the CSV file with captions and labels
        csv_path = hf_hub_download(
            repo_id="joshuachou/SkinCAP",
            filename="skincap_v240623.csv",
            repo_type="dataset",
            token=hf_token
        )
        
        print(f"Loading CSV file: {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Extract captions and labels from CSV
        # CSV columns: 'disease' (label), 'caption_zh_polish_en' (English caption)
        rows = []
        for _, row in df.iterrows():
            # Extract caption (English polished version)
            caption = row.get("caption_zh_polish_en") or row.get("caption_zh_polish") or ""
            # Extract label (disease name)
            label = row.get("disease") or ""
            
            # Skip if both are empty
            if caption or label:
                rows.append({
                    "caption": str(caption) if pd.notna(caption) else "",
                    "label": str(label) if pd.notna(label) else ""
                })
        
        if not rows:
            raise RuntimeError("No metadata found in CSV file.")
        
        print(f"Successfully loaded {len(rows)} metadata entries from SkinCAP dataset.")
        _dataset_cache = rows
        return rows
        
    except Exception as e:
        error_msg = str(e)
        if "403" in error_msg or "Forbidden" in error_msg:
            raise RuntimeError(
                "Access denied to SkinCAP dataset. "
                "Please ensure:\n"
                "1. You have accepted the dataset terms on https://huggingface.co/datasets/joshuachou/SkinCAP\n"
                "2. Your token has read access to the dataset\n"
                "3. You may need to request additional access for the metadata files"
            ) from e
        else:
            raise RuntimeError(
                f"Could not load SkinCAP dataset: {error_msg}. "
                "Please check your internet connection and token permissions."
            ) from e
