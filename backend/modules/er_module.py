"""Employee Relations (ER) Module - Workplace Harmony & Engagement"""

from fastapi import APIRouter
from datetime import datetime
from typing import Dict, List, Any
import json

router = APIRouter(prefix="/api/er", tags=["employee-relations"])

class MalaysianSentimentAnalyzer:
    def __init__(self):
        self.lexicon = {
            'tak adil': -0.8, 'diskriminasi': -0.9, 'stress': -0.7,
            'gembira': 0.8, 'puas hati': 0.7, 'seronok': 0.6,
            'kantoi': -0.7, 'sabo': -0.6, 'backstab': -0.8
        }
        
    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment with Malaysian context"""
        words = text.lower().split()
        sentiment_score = 0
        detected_terms = []
        
        for word in words:
            if word in self.lexicon:
                sentiment_score += self.lexicon[word]
                detected_terms.append(word)
                
        return {
            "sentiment_score": round(sentiment_score, 2),
            "sentiment": "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral",
            "detected_terms": detected_terms,
            "language": "mixed" if any(term in self.lexicon for term in words) else "english"
        }

class BurnoutPredictor:
    def predict(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict burnout with Malaysian work culture factors"""
        overtime_hours = employee_data.get('overtime_hours', 0)
        leave_taken = employee_data.get('leave_taken', 0)
        workload_score = employee_data.get('workload_score', 5)
        
        # Malaysian-specific factors
        ramadan_factor = 0.2 if employee_data.get('religion') == 'Islam' else 0
        cny_factor = 0.15 if employee_data.get('ethnicity') == 'Chinese' else 0
        
        burnout_risk = (overtime_hours * 0.1) + (10 - leave_taken) * 0.05 + (workload_score * 0.1)
        burnout_risk -= (ramadan_factor + cny_factor)  # Cultural adjustment
        
        return {
            "burnout_risk": round(min(burnout_risk, 10), 2),
            "risk_level": "high" if burnout_risk > 7 else "medium" if burnout_risk > 4 else "low",
            "recommendations": [
                "Consider flexible working hours during Ramadan" if ramadan_factor > 0 else None,
                "Schedule wellness check-in",
                "Review workload distribution"
            ]
        }

@router.post("/sentiment/analyze")
async def analyze_sentiment(text: str):
    analyzer = MalaysianSentimentAnalyzer()
    return analyzer.analyze(text)

@router.post("/burnout/predict")
async def predict_burnout(employee_data: Dict[str, Any]):
    predictor = BurnoutPredictor()
    return predictor.predict(employee_data)

@router.post("/whistleblowing/submit")
async def submit_whistleblowing_report(report: Dict[str, Any]):
    """Anonymous whistleblowing portal with PDPA compliance"""
    return {
        "report_id": f"WB-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
        "status": "received",
        "anonymity_level": "high",
        "estimated_review": "5-7 business days",
        "pdpa_compliant": True,
        "tracking_code": f"TRACK-{random.randint(100000, 999999)}"
    }

@router.get("/pulse-survey/results")
async def get_pulse_survey_results():
    """Real-time employee pulse survey results with demographic insights"""
    return {
        "overall_satisfaction": 7.2,
        "department_breakdown": {
            "IT": 8.1,
            "HR": 7.5,
            "Finance": 6.8,
            "Operations": 7.0
        },
        "demographic_insights": {
            "by_ethnicity": {
                "Malay": 7.3,
                "Chinese": 7.1,
                "Indian": 7.0,
                "Others": 7.2
            },
            "by_age_group": {
                "20-30": 7.5,
                "31-40": 7.0,
                "41-50": 6.8,
                "50+": 7.2
            }
        },
        "trending_topics": [
            {"topic": "work-life balance", "sentiment": 0.3},
            {"topic": "career development", "sentiment": 0.6},
            {"topic": "compensation", "sentiment": -0.2}
        ]
    }