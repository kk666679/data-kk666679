from huggingface_hub import HfApi, list_models
from transformers import pipeline
from typing import Dict, List
import requests

class HuggingFaceAnalyzer:
    def __init__(self):
        self.api = HfApi()
        
    def analyze_repository_models(self) -> Dict:
        """Analyze HuggingFace models suitable for HRMS"""
        
        # Search for HR-relevant models
        hr_tasks = ["sentiment-analysis", "text-classification", "ner", "question-answering"]
        
        results = {}
        for task in hr_tasks:
            try:
                models = list(self.api.list_models(task=task, limit=5))
                results[task] = [
                    {
                        "id": model.modelId,
                        "downloads": getattr(model, 'downloads', 0),
                        "likes": getattr(model, 'likes', 0)
                    }
                    for model in models
                ]
            except:
                results[task] = []
        
        return results
    
    def test_sentiment_models(self) -> Dict:
        """Test sentiment analysis models for HR use"""
        
        test_texts = [
            "Great work environment and supportive team",
            "Management is unfair and I want to quit",
            "Salary is competitive but workload is heavy"
        ]
        
        models_to_test = [
            "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "nlptown/bert-base-multilingual-uncased-sentiment"
        ]
        
        results = {}
        for model_id in models_to_test:
            try:
                classifier = pipeline("sentiment-analysis", model=model_id)
                model_results = []
                
                for text in test_texts:
                    prediction = classifier(text)[0]
                    model_results.append({
                        "text": text,
                        "label": prediction["label"],
                        "score": round(prediction["score"], 3)
                    })
                
                results[model_id] = model_results
            except Exception as e:
                results[model_id] = {"error": str(e)}
        
        return results
    
    def recommend_models_for_hrms(self) -> Dict:
        """Recommend best HuggingFace models for HRMS Malaysia"""
        
        recommendations = {
            "sentiment_analysis": {
                "primary": "cardiffnlp/twitter-roberta-base-sentiment-latest",
                "alternative": "nlptown/bert-base-multilingual-uncased-sentiment",
                "reason": "Robust sentiment detection for employee feedback"
            },
            "named_entity_recognition": {
                "primary": "dbmdz/bert-large-cased-finetuned-conll03-english",
                "alternative": "microsoft/DialoGPT-medium",
                "reason": "Extract names, organizations, locations from HR documents"
            },
            "text_classification": {
                "primary": "microsoft/DialoGPT-medium",
                "alternative": "distilbert-base-uncased",
                "reason": "Classify HR queries and route to appropriate agents"
            },
            "embeddings": {
                "primary": "sentence-transformers/all-MiniLM-L6-v2",
                "alternative": "sentence-transformers/all-mpnet-base-v2",
                "reason": "Semantic search for resumes and job matching"
            }
        }
        
        return recommendations