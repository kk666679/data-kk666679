from transformers import pipeline, AutoTokenizer, AutoModel
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import torch
import numpy as np
from typing import Dict, List, Optional

class EnhancedAIServices:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Enhanced sentiment analysis for Malaysian context
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # NER for Malaysian entities
        self.ner_pipeline = pipeline(
            "ner",
            model="dbmdz/bert-large-cased-finetuned-conll03-english",
            aggregation_strategy="simple",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Embeddings for semantic search
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
    def analyze_employee_feedback(self, feedback_text: str) -> Dict:
        """Enhanced sentiment analysis with confidence scoring"""
        result = self.sentiment_analyzer(feedback_text)
        
        # Extract key topics using NER
        entities = self.ner_pipeline(feedback_text)
        
        return {
            "sentiment": result[0]["label"],
            "confidence": round(result[0]["score"], 3),
            "entities": entities,
            "risk_level": self._calculate_risk_level(result[0])
        }
    
    def _calculate_risk_level(self, sentiment_result: Dict) -> str:
        """Calculate employee risk level based on sentiment"""
        if sentiment_result["label"] == "NEGATIVE" and sentiment_result["score"] > 0.8:
            return "HIGH"
        elif sentiment_result["label"] == "NEGATIVE" and sentiment_result["score"] > 0.6:
            return "MEDIUM"
        return "LOW"
    
    def smart_resume_matching(self, job_description: str, resumes: List[str]) -> List[Dict]:
        """AI-powered resume matching with similarity scores"""
        job_embedding = self.embeddings.embed_query(job_description)
        
        matches = []
        for i, resume in enumerate(resumes):
            resume_embedding = self.embeddings.embed_query(resume)
            similarity = np.dot(job_embedding, resume_embedding)
            
            matches.append({
                "resume_id": i,
                "similarity_score": round(float(similarity), 3),
                "match_quality": self._get_match_quality(similarity)
            })
        
        return sorted(matches, key=lambda x: x["similarity_score"], reverse=True)
    
    def _get_match_quality(self, score: float) -> str:
        """Convert similarity score to match quality"""
        if score > 0.8:
            return "EXCELLENT"
        elif score > 0.6:
            return "GOOD"
        elif score > 0.4:
            return "FAIR"
        return "POOR"
    
    def predict_employee_attrition(self, employee_data: Dict) -> Dict:
        """Simple attrition prediction model"""
        risk_factors = 0
        
        # Simplified risk calculation
        if employee_data.get("tenure_months", 0) < 12:
            risk_factors += 1
        if employee_data.get("satisfaction_score", 5) < 3:
            risk_factors += 2
        if employee_data.get("salary_percentile", 50) < 25:
            risk_factors += 1
        
        attrition_risk = min(risk_factors * 0.25, 1.0)
        
        return {
            "attrition_probability": round(attrition_risk, 3),
            "risk_level": "HIGH" if attrition_risk > 0.7 else "MEDIUM" if attrition_risk > 0.4 else "LOW",
            "recommendations": self._get_retention_recommendations(attrition_risk)
        }
    
    def _get_retention_recommendations(self, risk: float) -> List[str]:
        """Generate retention recommendations based on risk level"""
        if risk > 0.7:
            return [
                "Schedule immediate 1-on-1 meeting",
                "Review compensation package",
                "Discuss career development opportunities"
            ]
        elif risk > 0.4:
            return [
                "Conduct satisfaction survey",
                "Provide additional training opportunities"
            ]
        return ["Continue regular check-ins"]