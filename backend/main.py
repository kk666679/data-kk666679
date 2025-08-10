"""HRMS Malaysia FastAPI Application"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="HRMS Malaysia",
    description="AI-Powered Human Resource Management System for Malaysian Businesses",
    version="3.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "3.0.1"}

@app.post("/api/payroll/epf")
async def calculate_epf(data: dict):
    salary = data.get("salary", 0)
    employee_contribution = salary * 0.11  # 11%
    employer_contribution = salary * 0.13   # 13%
    
    return {
        "employee_contribution": employee_contribution,
        "employer_contribution": employer_contribution,
        "total": employee_contribution + employer_contribution
    }

@app.post("/api/ai/sentiment")
async def analyze_sentiment(data: dict):
    text = data.get("text", "")
    # Simple sentiment analysis
    positive_words = ["gembira", "senang", "baik", "bagus", "happy", "good"]
    sentiment = "positive" if any(word in text.lower() for word in positive_words) else "neutral"
    
    return {
        "sentiment": sentiment,
        "language": "ms" if any(word in text for word in ["saya", "di", "ini"]) else "en",
        "confidence": 0.85
    }

@app.get("/api/i18n/{lang}")
async def get_translations(lang: str):
    translations = {
        "en": {"welcome": "Welcome", "dashboard": "Dashboard"},
        "ms": {"welcome": "Selamat Datang", "dashboard": "Papan Pemuka"},
        "zh": {"welcome": "欢迎", "dashboard": "仪表板"}
    }
    return {"messages": translations.get(lang, translations["en"])}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)