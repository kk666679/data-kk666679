import spacy
from typing import Dict, List

class MalaysianResumeParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.malaysian_universities = [
            "Universiti Malaya", "UM", "Universiti Sains Malaysia", "USM",
            "Taylor's University", "Sunway University", "UTAR", "MMU"
        ]
    
    def parse_resume(self, resume_text: str) -> Dict:
        doc = self.nlp(resume_text)
        
        return {
            "skills": self._extract_skills(doc),
            "education": self._extract_education(resume_text),
            "experience_years": self._calculate_experience(doc),
            "university": self._identify_university(resume_text)
        }
    
    def _extract_skills(self, doc) -> List[str]:
        # Simplified skill extraction
        skills = []
        skill_keywords = ["Python", "Java", "SQL", "Excel", "Leadership"]
        for token in doc:
            if token.text in skill_keywords:
                skills.append(token.text)
        return skills
    
    def _extract_education(self, text: str) -> str:
        for uni in self.malaysian_universities:
            if uni.lower() in text.lower():
                return uni
        return "Unknown"
    
    def _calculate_experience(self, doc) -> int:
        # Simplified experience calculation
        return 3  # Default
    
    def _identify_university(self, text: str) -> str:
        for uni in self.malaysian_universities:
            if uni.lower() in text.lower():
                return uni
        return "Other"

class CandidateScoring:
    def calculate_ai_score(self, candidate_data: Dict) -> float:
        # Simplified ML scoring
        base_score = 0.5
        
        # Skills match bonus
        if len(candidate_data.get("skills", [])) > 3:
            base_score += 0.2
        
        # Local university bonus
        if candidate_data.get("university") in ["UM", "USM", "Taylor's"]:
            base_score += 0.1
        
        # Experience bonus
        if candidate_data.get("experience_years", 0) > 2:
            base_score += 0.2
        
        return min(base_score, 1.0)