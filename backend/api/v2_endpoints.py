from fastapi import APIRouter

router = APIRouter(prefix="/api/v2", tags=["v2"])

@router.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}

@router.get("/modules")
async def get_modules():
    return {
        "modules": ["IR", "ER", "L&D", "TA", "Payroll"],
        "status": "active"
    }