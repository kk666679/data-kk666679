from fastapi import APIRouter

router = APIRouter(prefix="/api/nlp", tags=["nlp"])

@router.post("/analyze-text")
async def analyze_text(text: str):
    return {
        "text": text,
        "language": "en" if any(c.isascii() for c in text) else "ms",
        "sentiment": "neutral",
        "confidence": 0.8
    }