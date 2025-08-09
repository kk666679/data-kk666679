from fastapi import FastAPI, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from core.models import DisputeCase, PulseSurvey, HRDFCourse, EPFCalculation
from core.malaysian_compliance import MalaysianCompliance
from core.ai_services import MalaysianAIServices
from api.v2_endpoints import router as v2_router
from api.nlp_endpoints import router as nlp_router
from api.blockchain_endpoints import router as blockchain_router
from monitoring.metrics import get_metrics, track_metrics

app = FastAPI(
    title="HRMS Malaysia API",
    description="AI-powered Human Resource Management System for Malaysian Businesses",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_services = MalaysianAIServices()

# Include routers
app.include_router(v2_router)
app.include_router(nlp_router)
app.include_router(blockchain_router)

@app.get("/")
async def root():
    return {"message": "HRMS Malaysia API v2.0 - AI Powered"}

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(get_metrics(), media_type="text/plain")

@app.post("/api/epf-calculator")
async def calculate_epf(calculation: EPFCalculation):
    """EPF Calculation API Endpoint"""
    return MalaysianCompliance.calculate_epf(calculation)

@app.post("/api/socso-calculator")
async def calculate_socso(basic_salary: float):
    """SOCSO Calculation API Endpoint"""
    return MalaysianCompliance.calculate_socso(basic_salary)

@app.post("/api/ir/pk-form")
async def generate_pk_form(case: DisputeCase):
    """Auto-generate JTK PK Form"""
    return await MalaysianCompliance.auto_fill_pk_form(case)

@app.post("/api/er/sentiment-analysis")
async def analyze_sentiment(survey: PulseSurvey):
    """Employee sentiment analysis"""
    return ai_services.analyze_employee_sentiment(survey)

@app.post("/api/ld/hrdf-claim")
async def calculate_hrdf_claim(course: HRDFCourse, levy_balance: float):
    """Calculate HRDF claim amount"""
    claimable = MalaysianCompliance.claim_hrdf(course, levy_balance)
    return {"claimable_amount": claimable, "course": course.model_dump()}

@app.post("/api/ta/parse-resume")
async def parse_resume(resume_text: str):
    """Parse Malaysian resume with AI"""
    return ai_services.parse_local_resume(resume_text)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "ai_services": "loaded"}