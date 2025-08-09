from transformers import pipeline
import pandas as pd
from typing import Dict, List
from .models import PulseSurvey, MalaysianResume

class MalaysianAIServices:
    def __init__(self):
        self.sentiment_analyzer = pipeline(
            "text-classification",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        
    def analyze_employee_sentiment(self, survey: PulseSurvey) -> Dict:
        """Malaysian dialect-specific sentiment analysis"""
        if not survey.comments:
            return {"sentiment": "neutral", "confidence": 0.5}
            
        results = self.sentiment_analyzer(" ".join(survey.comments))
        return {
            "department": survey.department,
            "sentiment": results[0]["label"],
            "confidence": results[0]["score"]
        }
    
    def parse_local_resume(self, text: str) -> Dict:
        """Extracts Malaysian-specific resume data"""
        malaysian_universities = [
            "Universiti Malaya", "UM", "Universiti Sains Malaysia", "USM",
            "Taylor's University", "Sunway University", "UTAR", "MMU"
        ]
        
        # Simple extraction logic
        university = "Other"
        for uni in malaysian_universities:
            if uni.lower() in text.lower():
                university = uni
                break
                
        return {
            "university": university,
            "skills": self._extract_skills(text),
            "experience_years": self._estimate_experience(text)
        }
    
    def _extract_skills(self, text: str) -> List[str]:
        common_skills = ["Python", "Java", "SQL", "Excel", "Leadership", "Communication"]
        return [skill for skill in common_skills if skill.lower() in text.lower()]
    
    def _estimate_experience(self, text: str) -> int:
        # Simple heuristic
        if "senior" in text.lower() or "lead" in text.lower():
            return 5
        elif "junior" in text.lower() or "fresh" in text.lower():
            return 1
        return 3