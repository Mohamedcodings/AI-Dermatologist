# Skin AI Dermatologist

An AI-powered dermatology assistant that analyzes skin images using Mistral Vision and matches them against the SkinCAP dataset.

## Features

- 🔍 **Vision Analysis**: Uses Mistral's Pixtral model to analyze skin images
- 📊 **Condition Matching**: Searches 4,000+ SkinCAP entries to find the most probable condition
- 🚀 **FastAPI Backend**: RESTful API with interactive documentation
- 🔒 **Secure**: Environment variables for API keys (never committed)

## Architecture

```
User uploads image → FastAPI
    ↓
Mistral Vision API (describes image)
    ↓
SkinCAP Dataset Search (finds matches)
    ↓
Returns top condition + disclaimer
```

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mohamedcodings/AI-Dermatologist.git
   cd AI-Dermatologist
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys:
   # - HF_TOKEN: Your Hugging Face token (for SkinCAP dataset access)
   # - MISTRAL_API_KEY: Your Mistral API key (for vision analysis)
   ```

5. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the API**
   - Interactive docs: http://127.0.0.1:8000/docs
   - Health check: http://127.0.0.1:8000/health
   - API endpoint: POST http://127.0.0.1:8000/api/skin/analyze

## API Usage

### Upload and analyze an image

```bash
curl -X POST \
  'http://127.0.0.1:8000/api/skin/analyze' \
  -H 'accept: application/json' \
  -F 'file=@your-image.jpg;type=image/jpeg'
```

### Response format

```json
{
  "vision_description": "Description from Mistral Vision...",
  "predicted_condition": "condition-name",
  "match_score": 18,
  "example_caption": "Matching caption from dataset...",
  "top_matches": [...],
  "disclaimer": "This is not a medical diagnosis..."
}
```

## Project Structure

```
skin-ai-dermatologist/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   └── skin.py          # HTTP endpoints
│   ├── services/
│   │   ├── dermatologist.py # Orchestration logic
│   │   ├── vision_client.py # Mistral Vision API
│   │   ├── skincap_loader.py # Dataset loader
│   │   └── skincap_matcher.py # Search/matching
│   └── core/
│       └── llm_client.py    # Optional LLM client
├── requirements.txt
├── .env.example
└── README.md
```

## Requirements

- Python 3.8+
- FastAPI
- Mistral API key (for vision analysis)
- Hugging Face token (for SkinCAP dataset access)

## Important Notes

⚠️ **This is not a medical diagnosis tool.** Always consult with healthcare professionals for actual medical advice.

## License

[Add your license here]

