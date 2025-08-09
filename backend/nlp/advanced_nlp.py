from transformers import pipeline
from sentence_transformers import SentenceTransformer
import spacy
from typing import Dict, List
import re

class AdvancedNLPEngine:
    def __init__(self):
        self.sentiment_model = pipeline("sentiment-analysis", return_all_scores=True)
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.nlp = spacy.load("en_core_web_sm")
        
        self.malaysian_patterns = {
            'ic_number': r'\d{6}-\d{2}-\d{4}',
            'universities': ['UM', 'USM', 'UKM', 'UTM', 'Taylor\'s', 'Sunway']
        }
    
    def analyze_employee_feedback(self, text: str) -> Dict:
        sentiment_scores = self.sentiment_model(text)[0]
        primary_sentiment = max(sentiment_scores, key=lambda x: x['score'])
        
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        risk_score = self._calculate_risk(text, sentiment_scores)
        
        return {
            "sentiment": primary_sentiment['label'],
            "confidence": round(primary_sentiment['score'], 3),
            "entities": entities,
            "risk_score": risk_score,
            "risk_level": "HIGH" if risk_score > 0.7 else "MEDIUM" if risk_score > 0.4 else "LOW"
        }
    
    def semantic_job_matching(self, job_description: str, resumes: List[str]) -> List[Dict]:
        from sklearn.metrics.pairwise import cosine_similarity
        
        job_embedding = self.sentence_model.encode([job_description])
        resume_embeddings = self.sentence_model.encode(resumes)
        similarities = cosine_similarity(job_embedding, resume_embeddings)[0]
        
        matches = []
        for i, similarity in enumerate(similarities):
            matches.append({
                "resume_id": i,
                "similarity_score": round(float(similarity), 3),
                "match_quality": "EXCELLENT" if similarity > 0.8 else "GOOD" if similarity > 0.6 else "FAIR"
            })
        
        return sorted(matches, key=lambda x: x["similarity_score"], reverse=True)
    
    def _calculate_risk(self, text: str, sentiments: List[Dict]) -> float:
        negative_score = next((s['score'] for s in sentiments if s['label'] == 'NEGATIVE'), 0)
        risk_words = ['quit', 'resign', 'unfair', 'harassment']
        risk_mentions = sum(1 for word in risk_words if word.lower() in text.lower())
        return min(negative_score + (risk_mentions * 0.2), 1.0)