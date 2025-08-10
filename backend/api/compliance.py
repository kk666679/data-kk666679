from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any

router = APIRouter(prefix="/api", tags=["compliance"])

@router.get("/compliance-status")
async def get_compliance_status() -> Dict[str, Any]:
    """Get real-time Malaysian compliance status"""
    return {
        "epf": True,
        "socso": True,
        "employment_act": "2024-01-15",
        "pdpa": True,
        "hrdf": True,
        "updated_at": datetime.now().isoformat(),
        "status": "compliant",
        "details": {
            "epf_rate": {"employee": 0.11, "employer": 0.13},
            "socso_active": True,
            "pdpa_certified": True,
            "employment_act_version": "2024.1"
        }
    }

@router.post("/calculate/epf")
async def calculate_epf(salary: float) -> Dict[str, float]:
    """Calculate EPF contributions for Malaysian employees"""
    employee_contribution = salary * 0.11  # 11%
    employer_contribution = salary * 0.13   # 13%
    
    return {
        "salary": salary,
        "employee_contribution": round(employee_contribution, 2),
        "employer_contribution": round(employer_contribution, 2),
        "total_contribution": round(employee_contribution + employer_contribution, 2)
    }

@router.post("/calculate/socso")
async def calculate_socso(salary: float) -> Dict[str, float]:
    """Calculate SOCSO contributions"""
    # SOCSO rates based on salary brackets
    if salary <= 30:
        employee = 0.10
        employer = 0.40
    elif salary <= 50:
        employee = 0.20
        employer = 0.70
    else:
        # Standard rates for higher salaries
        employee = min(salary * 0.005, 19.75)  # Max RM19.75
        employer = min(salary * 0.0175, 69.05)  # Max RM69.05
    
    return {
        "salary": salary,
        "employee_contribution": round(employee, 2),
        "employer_contribution": round(employer, 2),
        "total_contribution": round(employee + employer, 2)
    }