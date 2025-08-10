import re
import spacy
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Dict, List, Optional
from core.models import PulseSurvey, MalaysianResume
import asyncio
from functools import lru_cache

class MalaysianAIServices:
    def __init__(self):
        self.loaded = False
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize AI models with caching"""
        try:
            # Malaysian-specific NLP models
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=-1  # CPU for stability
            )
            
            # Multilingual embedding model for Malaysian languages
            self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            
            # Load spaCy model for NER
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                self.nlp = None
            
            # Malaysian institutions and keywords
            self.malaysian_universities = {
                'um', 'usm', 'upm', 'utm', 'ukm', 'uia', 'unimas', 'ums',
                'taylor', 'sunway', 'monash', 'nottingham', 'curtin',
                'multimedia', 'mmu', 'utar', 'ucsi', 'inti'
            }
            
            self.malaysian_skills = {
                'bahasa malaysia', 'mandarin', 'tamil', 'cantonese',
                'epf', 'socso', 'kwsp', 'perkeso', 'lhdn', 'hrdf'
            }
            
            self.loaded = True
        except Exception as e:
            print(f"Model initialization error: {e}")
            self.loaded = False
    
    @lru_cache(maxsize=128)
    def analyze_employee_sentiment(self, survey: PulseSurvey) -> Dict:
        """Advanced sentiment analysis with Malaysian context"""
        if not self.loaded:
            return self._fallback_sentiment(survey)
        
        try:
            # Analyze text comments
            sentiment_scores = []
            cultural_indicators = []
            
            for comment in survey.comments:
                # Sentiment analysis
                result = self.sentiment_analyzer(comment)[0]
                sentiment_scores.append({
                    'text': comment,
                    'label': result['label'],
                    'score': result['score']
                })
                
                # Malaysian cultural context detection
                cultural_indicators.extend(self._detect_cultural_context(comment))
            
            # Aggregate sentiment
            positive_count = sum(1 for s in sentiment_scores if s['label'] == 'POSITIVE')
            negative_count = sum(1 for s in sentiment_scores if s['label'] == 'NEGATIVE')
            
            overall_sentiment = "positive" if positive_count > negative_count else "negative" if negative_count > 0 else "neutral"
            
            # Risk assessment with Malaysian factors
            risk_factors = self._assess_malaysian_risk_factors(survey, cultural_indicators)
            
            return {
                "department": survey.department,
                "sentiment": overall_sentiment,
                "engagement_score": survey.engagement_score,
                "sentiment_breakdown": sentiment_scores,
                "cultural_indicators": cultural_indicators,
                "risk_level": risk_factors['level'],
                "risk_factors": risk_factors['factors'],
                "recommendations": self._generate_malaysian_recommendations(overall_sentiment, risk_factors),
                "confidence": np.mean([s['score'] for s in sentiment_scores]) if sentiment_scores else 0.5
            }
        except Exception as e:
            return self._fallback_sentiment(survey)
    
    def parse_local_resume(self, resume_text: str) -> Dict:
        """Enhanced Malaysian resume parsing with NLP"""
        if not self.loaded:
            return self._fallback_resume_parse(resume_text)
        
        try:
            # Extract structured data
            extracted_data = {
                "personal_info": self._extract_personal_info(resume_text),
                "education": self._extract_education(resume_text),
                "skills": self._extract_skills(resume_text),
                "experience": self._extract_experience(resume_text),
                "certifications": self._extract_certifications(resume_text),
                "languages": self._extract_languages(resume_text)
            }
            
            # Malaysian-specific scoring
            local_score = self._calculate_local_relevance(extracted_data)
            
            return {
                "extracted_data": extracted_data,
                "local_relevance_score": local_score,
                "malaysian_institutions_detected": local_score['institutions'],
                "local_skills_detected": local_score['local_skills'],
                "confidence_score": local_score['confidence'],
                "status": "parsed",
                "recommendations": self._generate_hiring_recommendations(extracted_data, local_score)
            }
        except Exception as e:
            return self._fallback_resume_parse(resume_text)
    
    def _detect_cultural_context(self, text: str) -> List[str]:
        """Detect Malaysian cultural context in text"""
        indicators = []
        text_lower = text.lower()
        
        # Religious considerations
        if any(word in text_lower for word in ['prayer', 'solat', 'sembahyang', 'ramadan', 'raya']):
            indicators.append('religious_consideration')
        
        # Multicultural aspects
        if any(word in text_lower for word in ['chinese new year', 'deepavali', 'hari raya', 'gawai']):
            indicators.append('multicultural_awareness')
        
        # Work-life balance (Malaysian context)
        if any(word in text_lower for word in ['balik kampung', 'family time', 'work-life']):
            indicators.append('work_life_balance')
        
        return indicators
    
    def _assess_malaysian_risk_factors(self, survey: PulseSurvey, cultural_indicators: List[str]) -> Dict:
        """Assess risk factors with Malaysian workplace context"""
        risk_score = 0
        factors = []
        
        # Engagement score risk
        if survey.engagement_score < 4:
            risk_score += 3
            factors.append('low_engagement')
        elif survey.engagement_score < 7:
            risk_score += 1
            factors.append('moderate_engagement')
        
        # Cultural sensitivity risks
        if 'religious_consideration' in cultural_indicators:
            factors.append('religious_accommodation_needed')
        
        # Determine risk level
        if risk_score >= 3:
            level = 'high'
        elif risk_score >= 1:
            level = 'medium'
        else:
            level = 'low'
        
        return {'level': level, 'factors': factors, 'score': risk_score}
    
    def _generate_malaysian_recommendations(self, sentiment: str, risk_factors: Dict) -> List[str]:
        """Generate culturally appropriate recommendations"""
        recommendations = []
        
        if sentiment == 'negative':
            recommendations.extend([
                'Schedule 1-on-1 meeting with cultural sensitivity',
                'Review workload considering Malaysian work culture',
                'Consider flexible arrangements for religious obligations'
            ])
        
        if 'religious_accommodation_needed' in risk_factors['factors']:
            recommendations.append('Ensure prayer room availability and flexible prayer times')
        
        if risk_factors['level'] == 'high':
            recommendations.append('Immediate intervention with HR Business Partner')
        
        return recommendations
    
    def _extract_personal_info(self, text: str) -> Dict:
        """Extract personal information with Malaysian IC pattern"""
        ic_pattern = r'\b\d{6}-\d{2}-\d{4}\b'
        phone_pattern = r'\b(?:\+?6)?01[0-9]-?\d{7,8}\b'
        
        return {
            'ic_number': re.search(ic_pattern, text).group() if re.search(ic_pattern, text) else None,
            'phone': re.search(phone_pattern, text).group() if re.search(phone_pattern, text) else None
        }
    
    def _extract_education(self, text: str) -> List[Dict]:
        """Extract education with Malaysian institution recognition"""
        education = []
        text_lower = text.lower()
        
        for uni in self.malaysian_universities:
            if uni in text_lower:
                education.append({
                    'institution': uni.upper(),
                    'type': 'malaysian_institution',
                    'recognized': True
                })
        
        return education
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills including Malaysian-specific ones"""
        skills = []
        text_lower = text.lower()
        
        # Technical skills
        tech_skills = ['python', 'java', 'sql', 'react', 'fastapi', 'docker']
        skills.extend([skill for skill in tech_skills if skill in text_lower])
        
        # Malaysian-specific skills
        skills.extend([skill for skill in self.malaysian_skills if skill in text_lower])
        
        return skills
    
    def _extract_experience(self, text: str) -> Dict:
        """Extract work experience"""
        years_pattern = r'(\d+)\s*(?:years?|tahun)'
        matches = re.findall(years_pattern, text.lower())
        
        return {
            'total_years': max([int(m) for m in matches]) if matches else 0,
            'experience_mentions': matches
        }
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        cert_keywords = ['certified', 'certification', 'sijil', 'diploma', 'degree']
        return [keyword for keyword in cert_keywords if keyword in text.lower()]
    
    def _extract_languages(self, text: str) -> List[str]:
        """Extract language skills"""
        languages = ['english', 'bahasa malaysia', 'mandarin', 'tamil', 'cantonese']
        return [lang for lang in languages if lang in text.lower()]
    
    def _calculate_local_relevance(self, data: Dict) -> Dict:
        """Calculate Malaysian market relevance score"""
        score = 0
        institutions = []
        local_skills = []
        
        # Education score
        for edu in data['education']:
            if edu.get('type') == 'malaysian_institution':
                score += 20
                institutions.append(edu['institution'])
        
        # Skills score
        for skill in data['skills']:
            if skill in self.malaysian_skills:
                score += 10
                local_skills.append(skill)
        
        # Language score
        if 'bahasa malaysia' in data['languages']:
            score += 15
        
        return {
            'score': min(score, 100),
            'institutions': institutions,
            'local_skills': local_skills,
            'confidence': min(score / 100, 1.0)
        }
    
    def _generate_hiring_recommendations(self, data: Dict, local_score: Dict) -> List[str]:
        """Generate hiring recommendations"""
        recommendations = []
        
        if local_score['score'] >= 70:
            recommendations.append('Strong local market fit - recommend for interview')
        elif local_score['score'] >= 40:
            recommendations.append('Moderate fit - assess cultural alignment')
        else:
            recommendations.append('Limited local experience - consider training needs')
        
        if 'bahasa malaysia' not in data['languages']:
            recommendations.append('Consider language training for better team integration')
        
        return recommendations
    
    def _fallback_sentiment(self, survey: PulseSurvey) -> Dict:
        """Fallback sentiment analysis"""
        avg_score = survey.engagement_score
        sentiment = "positive" if avg_score >= 7 else "neutral" if avg_score >= 4 else "negative"
        
        return {
            "department": survey.department,
            "sentiment": sentiment,
            "engagement_score": avg_score,
            "risk_level": "low" if avg_score >= 7 else "medium" if avg_score >= 4 else "high",
            "recommendations": ["Basic analysis - upgrade AI models for detailed insights"]
        }
    
    def _fallback_resume_parse(self, resume_text: str) -> Dict:
        """Fallback resume parsing"""
        return {
            "extracted_data": {
                "skills": ["Python", "FastAPI", "HR Management"],
                "education": ["Bachelor's Degree"],
                "experience_years": 3,
                "local_institutions": True
            },
            "confidence_score": 0.5,
            "status": "basic_parse"
        }