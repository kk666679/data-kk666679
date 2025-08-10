import pytest
import asyncio
import httpx
from core.malaysian_compliance import MalaysianCompliance
from integrations.malaysian_apis import MalaysianAPIIntegration

class TestMalaysianIntegration:
    
    @pytest.fixture
    def api_client(self):
        return httpx.AsyncClient(base_url="http://localhost:8000")
    
    @pytest.mark.asyncio
    async def test_epf_calculation(self, api_client):
        """Test EPF calculation endpoint"""
        response = await api_client.post("/api/epf-calculator", json={
            "basic_salary": 5000,
            "employee_rate": 0.11,
            "employer_rate": 0.13
        })
        assert response.status_code == 200
        data = response.json()
        assert data["employee_contribution"] == 550
        assert data["employer_contribution"] == 650
    
    @pytest.mark.asyncio
    async def test_socso_calculation(self, api_client):
        """Test SOCSO calculation endpoint"""
        response = await api_client.post("/api/socso-calculator", json={
            "basic_salary": 5000
        })
        assert response.status_code == 200
        data = response.json()
        assert "employee_premium" in data
        assert "employer_premium" in data
    
    @pytest.mark.asyncio
    async def test_hrdf_claim(self, api_client):
        """Test HRDF claim calculation"""
        response = await api_client.post("/api/ld/hrdf-claim", json={
            "code": "TECH001",
            "hours": 40,
            "provider": "TechTraining Sdn Bhd",
            "claimable_amount": 2000
        })
        assert response.status_code == 200
        data = response.json()
        assert "claimable_amount" in data
    
    @pytest.mark.asyncio
    async def test_sentiment_analysis(self, api_client):
        """Test Malaysian sentiment analysis"""
        response = await api_client.post("/api/er/sentiment-analysis", json={
            "department": "IT",
            "engagement_score": 7.5,
            "comments": ["Kerja bagus", "Team spirit excellent"]
        })
        assert response.status_code == 200
        data = response.json()
        assert "sentiment" in data
        assert "cultural_indicators" in data
    
    @pytest.mark.asyncio
    async def test_resume_parsing(self, api_client):
        """Test Malaysian resume parsing"""
        resume_text = """
        John Lim Wei Ming
        IC: 901234-56-7890
        Education: Bachelor of Computer Science, Universiti Malaya
        Skills: Python, Bahasa Malaysia, Mandarin
        Experience: 3 years software development
        """
        
        response = await api_client.post("/api/ta/parse-resume", json={
            "resume_text": resume_text
        })
        assert response.status_code == 200
        data = response.json()
        assert "local_relevance_score" in data
        assert "malaysian_institutions_detected" in data

class TestCompliance:
    
    def test_epf_rates(self):
        """Test EPF rate calculations"""
        compliance = MalaysianCompliance()
        rates = compliance.get_current_epf_rates()
        assert rates["employee"] == 0.11
        assert rates["employer"] == 0.13
    
    def test_socso_calculation(self):
        """Test SOCSO premium calculation"""
        compliance = MalaysianCompliance()
        premium = compliance.calculate_socso(5000)
        assert premium["employee"] > 0
        assert premium["employer"] > 0
    
    def test_pcb_calculation(self):
        """Test PCB tax calculation"""
        compliance = MalaysianCompliance()
        pcb = compliance.calculate_pcb(5000, "single")
        assert pcb >= 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])