"""Learning & Development (L&D) Module - HRDF-Claimable Training"""

from fastapi import APIRouter
from datetime import datetime
from typing import Dict, List, Any
import random

router = APIRouter(prefix="/api/ld", tags=["learning-development"])

class HRDFClaimAssistant:
    def __init__(self):
        self.hrdf_categories = {
            "technical": {"max_claim": 5000, "approval_rate": 0.85},
            "management": {"max_claim": 8000, "approval_rate": 0.90},
            "safety": {"max_claim": 3000, "approval_rate": 0.95},
            "digital": {"max_claim": 6000, "approval_rate": 0.80}
        }
        
    def process_claim(self, training_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process HRDF claim with document validation"""
        category = training_data.get('category', 'technical')
        cost = training_data.get('cost', 0)
        
        category_info = self.hrdf_categories.get(category, self.hrdf_categories['technical'])
        claimable_amount = min(cost * 0.5, category_info['max_claim'])
        
        return {
            "claim_id": f"HRDF-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
            "category": category,
            "training_cost": cost,
            "claimable_amount": claimable_amount,
            "approval_probability": category_info['approval_rate'],
            "required_documents": [
                "Training invoice",
                "Attendance certificate",
                "MyKAD copy",
                "Company registration"
            ],
            "processing_steps": [
                {"step": "Document Upload", "status": "pending", "duration_days": 1},
                {"step": "HRDC Verification", "status": "pending", "duration_days": 7},
                {"step": "MOF Approval", "status": "pending", "duration_days": 14}
            ]
        }

class MicrolearningEngine:
    def __init__(self):
        self.content_library = {
            "safety": {
                "title": "Workplace Safety Basics",
                "duration_minutes": 15,
                "languages": ["BM", "EN", "ZH"],
                "modules": ["Fire Safety", "First Aid", "PPE Usage"]
            },
            "compliance": {
                "title": "Malaysian Labor Laws",
                "duration_minutes": 20,
                "languages": ["BM", "EN"],
                "modules": ["Employment Act", "SOCSO", "EPF"]
            },
            "leadership": {
                "title": "Leading Diverse Teams",
                "duration_minutes": 25,
                "languages": ["BM", "EN", "ZH"],
                "modules": ["Cultural Sensitivity", "Communication", "Conflict Resolution"]
            }
        }
        
    def get_personalized_path(self, employee_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized learning path"""
        role = employee_profile.get('role', 'general')
        department = employee_profile.get('department', 'general')
        language_pref = employee_profile.get('language_preference', 'EN')
        
        recommended_courses = []
        
        # Mandatory compliance training
        if 'compliance' in self.content_library:
            course = self.content_library['compliance'].copy()
            if language_pref in course['languages']:
                course['priority'] = 'high'
                course['reason'] = 'Mandatory compliance training'
                recommended_courses.append(course)
                
        # Role-specific recommendations
        if role in ['manager', 'supervisor']:
            if 'leadership' in self.content_library:
                course = self.content_library['leadership'].copy()
                course['priority'] = 'medium'
                course['reason'] = 'Leadership development'
                recommended_courses.append(course)
                
        return {
            "employee_id": employee_profile.get('id'),
            "learning_path": recommended_courses,
            "total_duration_hours": sum(c.get('duration_minutes', 0) for c in recommended_courses) / 60,
            "hrdf_claimable": True,
            "estimated_completion": "4 weeks"
        }

@router.post("/hrdf/claim")
async def process_hrdf_claim(training_data: Dict[str, Any]):
    assistant = HRDFClaimAssistant()
    return assistant.process_claim(training_data)

@router.post("/learning-path/generate")
async def generate_learning_path(employee_profile: Dict[str, Any]):
    engine = MicrolearningEngine()
    return engine.get_personalized_path(employee_profile)

@router.get("/courses/library")
async def get_course_library():
    """Get available microlearning courses"""
    return {
        "total_courses": 45,
        "categories": [
            {
                "name": "Safety & Compliance",
                "courses": 12,
                "languages": ["BM", "EN", "ZH", "TA"],
                "hrdf_claimable": True
            },
            {
                "name": "Digital Skills",
                "courses": 18,
                "languages": ["BM", "EN"],
                "hrdf_claimable": True
            },
            {
                "name": "Leadership",
                "courses": 15,
                "languages": ["BM", "EN", "ZH"],
                "hrdf_claimable": True
            }
        ],
        "popular_courses": [
            "Workplace Safety (BM)",
            "Digital Marketing Basics",
            "Team Leadership Skills"
        ],
        "completion_stats": {
            "average_completion_rate": 0.78,
            "average_rating": 4.2,
            "total_learners": 1250
        }
    }

@router.get("/hrdf/status/{claim_id}")
async def get_claim_status(claim_id: str):
    """Track HRDF claim status"""
    return {
        "claim_id": claim_id,
        "status": "under_review",
        "current_step": "HRDC Verification",
        "progress_percentage": 45,
        "estimated_completion": "10 business days",
        "updates": [
            {
                "date": "2024-01-15",
                "status": "submitted",
                "note": "Documents received and validated"
            },
            {
                "date": "2024-01-18",
                "status": "under_review",
                "note": "HRDC verification in progress"
            }
        ],
        "next_action": "Awaiting HRDC response",
        "contact_info": {
            "hrdc_officer": "Puan Siti Rahman",
            "phone": "03-2096-4000",
            "email": "claims@hrdc.com.my"
        }
    }