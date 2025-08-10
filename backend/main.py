from fastapi import FastAPI, Depends, Response, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
from contextlib import asynccontextmanager
import logging
from core.models import DisputeCase, PulseSurvey, HRDFCourse, EPFCalculation
from core.malaysian_compliance import MalaysianCompliance
from core.ai_services import MalaysianAIServices
from api.v2_endpoints import router as v2_router
from api.nlp_endpoints import router as nlp_router
from api.blockchain_endpoints import router as blockchain_router
from monitoring.metrics import get_metrics, track_metrics
import os
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting HRMS Malaysia API v3.0")
    
    # Initialize Redis for rate limiting
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_client = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_client)
    
    # Initialize AI services
    global ai_services
    ai_services = MalaysianAIServices()
    logger.info(f"AI Services loaded: {ai_services.loaded}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down HRMS Malaysia API")
    await FastAPILimiter.close()

app = FastAPI(
    title="HRMS Malaysia API",
    description="AI-powered Human Resource Management System for Malaysian Businesses with full EPF/SOCSO/HRDF compliance",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "*.hrms-malaysia.com"]
)

# Performance middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# CORS middleware
allowed_origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://127.0.0.1:3000",
    "https://hrms-malaysia.com",
    "https://www.hrms-malaysia.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count", "X-Rate-Limit-Remaining"]
)

# Global variables
ai_services: Optional[MalaysianAIServices] = None

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