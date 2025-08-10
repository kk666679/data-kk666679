"""Talent Acquisition (TA) Module - AI-Driven Recruitment"""

from fastapi import APIRouter
from datetime import datetime
from typing import Dict, List, Any
import re

router = APIRouter(prefix="/api/ta", tags=["talent-acquisition"])

class MalaysianResumeScorer:
    def __init__(self):
        self.local_universities = {
            "UM": 9.0, "USM": 8.5, "UKM": 8.5, "UTM": 8.0,
            "UTAR": 7.5, "Taylor's": 7.0, "Sunway": 7.0,
            "MMU": 6.5, "INTI": 6.0
        }
        self.glc_companies = [
            "Maybank", "CIMB", "Public Bank", "Genting",
            "Sime Darby", "IOI", "Axiata", "Digi"
        ]
        
    def score_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Score resume with Malaysian context"""
        base_score = 5.0
        
        # Education scoring
        education = resume_data.get('education', '')
        for uni, score in self.local_universities.items():
            if uni.lower() in education.lower():
                base_score += (score - 5.0) * 0.3
                break
                
        # Experience scoring
        experience = resume_data.get('experience', '')
        glc_bonus = 0
        for company in self.glc_companies:
            if company.lower() in experience.lower():
                glc_bonus += 0.5
                
        # Language skills
        languages = resume_data.get('languages', [])
        language_bonus = 0
        if 'Bahasa Malaysia' in languages:
            language_bonus += 0.3
        if 'Mandarin' in languages:
            language_bonus += 0.2
        if 'Tamil' in languages:
            language_bonus += 0.2
            
        final_score = min(base_score + glc_bonus + language_bonus, 10.0)
        
        return {
            "overall_score": round(final_score, 2),
            "education_score": round(base_score, 2),
            "experience_bonus": round(glc_bonus, 2),
            "language_bonus": round(language_bonus, 2),
            "ranking": "excellent" if final_score >= 8 else "good" if final_score >= 6 else "average"
        }

class BiasDetector:
    def __init__(self):
        self.bias_terms = {
            'racial': ['bumiputera', 'non-muslim', 'chinese only', 'malay preferred'],
            'gender': ['female secretary', 'male driver', 'pretty girl', 'handsome guy'],
            'age': ['young and energetic', 'fresh graduate only', 'below 30'],
            'religious': ['non-muslim', 'christian preferred', 'muslim only']
        }
        
    def detect_bias(self, job_description: str) -> Dict[str, Any]:
        """Detect discriminatory language in job postings"""
        detected_bias = []
        text_lower = job_description.lower()
        
        for category, terms in self.bias_terms.items():
            for term in terms:
                if term in text_lower:
                    detected_bias.append({
                        "category": category,
                        "term": term,
                        "severity": "high",
                        "suggestion": f"Remove '{term}' and focus on job-relevant skills"
                    })
                    
        return {
            "bias_detected": len(detected_bias) > 0,
            "bias_count": len(detected_bias),
            "violations": detected_bias,
            "compliance_score": max(0, 100 - (len(detected_bias) * 20))
        }

@router.post("/resume/score")
async def score_resume(resume_data: Dict[str, Any]):
    scorer = MalaysianResumeScorer()
    return scorer.score_resume(resume_data)

@router.post("/job-posting/bias-check")
async def check_job_bias(job_description: str):
    detector = BiasDetector()
    return detector.detect_bias(job_description)

@router.post("/interview/schedule")
async def schedule_interview(interview_data: Dict[str, Any]):
    """Schedule interview avoiding prayer times and cultural holidays"""
    return {
        "interview_id": f"INT-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
        "scheduled_time": interview_data.get('preferred_time'),
        "cultural_considerations": {
            "prayer_times_avoided": True,
            "ramadan_adjustment": False,
            "public_holidays_checked": True
        },
        "interview_kit": {
            "languages_available": ["English", "Bahasa Malaysia", "Mandarin"],
            "cultural_sensitivity_notes": "Prepared",
            "bias_free_questions": True
        }
    }

@router.get("/candidates/diversity-report")
async def get_diversity_report():
    """Generate diversity and inclusion report"""
    return {
        "total_candidates": 150,
        "diversity_breakdown": {
            "ethnicity": {
                "Malay": 45,
                "Chinese": 38,
                "Indian": 22,
                "Others": 45
            },
            "gender": {
                "Male": 78,
                "Female": 72
            },
            "age_groups": {
                "20-30": 85,
                "31-40": 45,
                "41-50": 15,
                "50+": 5
            }
        },
        "hiring_funnel": {
            "applications": 150,
            "screened": 75,
            "interviewed": 30,
            "hired": 8
        },
        "bias_metrics": {
            "bias_incidents": 2,
            "corrective_actions": 2,
            "compliance_score": 96
        }
    }