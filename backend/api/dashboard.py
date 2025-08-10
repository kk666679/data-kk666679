from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any

router = APIRouter(prefix="/api", tags=["dashboard"])

@router.get("/dashboard")
async def get_unified_dashboard() -> Dict[str, Any]:
    """Get unified dashboard data from all modules"""
    return {
        "ir": {
            "active_cases": 12,
            "forms_generated": 8,
            "compliance_score": 95,
            "recent_cases": [
                {"id": "DC001", "type": "misconduct", "status": "mediation"},
                {"id": "DC002", "type": "unfair_dismissal", "status": "active"}
            ]
        },
        "er": {
            "overall_satisfaction": 7.2,
            "department_sentiment": [
                {"department": "IT", "score": 8.1},
                {"department": "HR", "score": 7.5},
                {"department": "Finance", "score": 6.8},
                {"department": "Operations", "score": 7.0}
            ],
            "burnout_alerts": 3,
            "pulse_response_rate": 85
        },
        "ta": {
            "funnel": {
                "applications": 150,
                "screened": 75,
                "interviewed": 30,
                "hired": 8
            },
            "diversity_score": 92,
            "bias_incidents": 2,
            "time_to_hire": 21
        },
        "ld": {
            "active_courses": 45,
            "completion_rate": 78,
            "hrdf_claims": {
                "approved": 60,
                "pending": 30,
                "rejected": 10
            },
            "total_training_hours": 2340
        },
        "payroll": {
            "monthly_total": "750000",
            "employees_processed": 150,
            "compliance_status": {
                "epf": True,
                "socso": True,
                "eis": True,
                "pcb": True
            },
            "statutory_summary": {
                "total_epf": 180000,
                "total_socso": 12825,
                "total_eis": 3000
            }
        },
        "real_time_updates": [
            {
                "timestamp": datetime.now().isoformat(),
                "module": "payroll",
                "message": "New EPF calculation completed for 15 employees",
                "type": "success"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "module": "ir",
                "message": "IR case DC001 moved to mediation phase",
                "type": "info"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "module": "ld",
                "message": "HRDF claim HRDF-002 approved - RM 2,500",
                "type": "success"
            }
        ],
        "system_health": {
            "api_response_time": "120ms",
            "database_status": "healthy",
            "active_users": 45,
            "last_backup": "2024-01-15T10:30:00Z"
        }
    }

@router.get("/dashboard/{module}")
async def get_module_dashboard(module: str) -> Dict[str, Any]:
    """Get specific module dashboard data"""
    full_data = await get_unified_dashboard()
    return {module: full_data.get(module, {})}

@router.get("/dashboard/metrics/summary")
async def get_dashboard_metrics() -> Dict[str, Any]:
    """Get key performance indicators across all modules"""
    return {
        "total_employees": 150,
        "active_cases": 12,
        "monthly_payroll": 750000,
        "training_completion": 78,
        "compliance_score": 96,
        "satisfaction_score": 7.2,
        "recruitment_efficiency": 85,
        "cost_per_hire": 2500,
        "updated_at": datetime.now().isoformat()
    }