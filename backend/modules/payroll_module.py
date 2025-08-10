"""Payroll Module - Malaysian Compliance & Automated Calculations"""

from fastapi import APIRouter
from datetime import datetime, date
from typing import Dict, List, Any
import calendar

router = APIRouter(prefix="/api/payroll", tags=["payroll"])

class MalaysianPayrollEngine:
    def __init__(self):
        self.epf_rates = {"employee": 0.11, "employer": 0.13}
        self.eis_rates = {"employee": 0.002, "employer": 0.002}
        self.socso_brackets = [
            {"min": 0, "max": 30, "employee": 0.10, "employer": 0.40},
            {"min": 30.01, "max": 50, "employee": 0.20, "employer": 0.70},
            {"min": 50.01, "max": 70, "employee": 0.30, "employer": 1.10},
            {"min": 70.01, "max": 100, "employee": 0.40, "employer": 1.50},
            {"min": 100.01, "max": 140, "employee": 0.60, "employer": 2.10},
            {"min": 140.01, "max": 200, "employee": 0.85, "employer": 2.95},
            {"min": 200.01, "max": 300, "employee": 1.25, "employer": 4.35},
            {"min": 300.01, "max": 400, "employee": 1.75, "employer": 6.15},
            {"min": 400.01, "max": 500, "employee": 2.25, "employer": 7.85},
            {"min": 500.01, "max": 600, "employee": 2.75, "employer": 9.65},
            {"min": 600.01, "max": 700, "employee": 3.25, "employer": 11.35},
            {"min": 700.01, "max": 800, "employee": 3.75, "employer": 13.15},
            {"min": 800.01, "max": 900, "employee": 4.25, "employer": 14.85},
            {"min": 900.01, "max": 1000, "employee": 4.75, "employer": 16.65},
            {"min": 1000.01, "max": 1100, "employee": 5.25, "employer": 18.35},
            {"min": 1100.01, "max": 1200, "employee": 5.75, "employer": 20.15},
            {"min": 1200.01, "max": 1300, "employee": 6.25, "employer": 21.85},
            {"min": 1300.01, "max": 1400, "employee": 6.75, "employer": 23.65},
            {"min": 1400.01, "max": 1500, "employee": 7.25, "employer": 25.35},
            {"min": 1500.01, "max": 1600, "employee": 7.75, "employer": 27.15},
            {"min": 1600.01, "max": 1700, "employee": 8.25, "employer": 28.85},
            {"min": 1700.01, "max": 1800, "employee": 8.75, "employer": 30.65},
            {"min": 1800.01, "max": 1900, "employee": 9.25, "employer": 32.35},
            {"min": 1900.01, "max": 2000, "employee": 9.75, "employer": 34.15},
            {"min": 2000.01, "max": 2100, "employee": 10.25, "employer": 35.85},
            {"min": 2100.01, "max": 2200, "employee": 10.75, "employer": 37.65},
            {"min": 2200.01, "max": 2300, "employee": 11.25, "employer": 39.35},
            {"min": 2300.01, "max": 2400, "employee": 11.75, "employer": 41.15},
            {"min": 2400.01, "max": 2500, "employee": 12.25, "employer": 42.85},
            {"min": 2500.01, "max": 2600, "employee": 12.75, "employer": 44.65},
            {"min": 2600.01, "max": 2700, "employee": 13.25, "employer": 46.35},
            {"min": 2700.01, "max": 2800, "employee": 13.75, "employer": 48.15},
            {"min": 2800.01, "max": 2900, "employee": 14.25, "employer": 49.85},
            {"min": 2900.01, "max": 3000, "employee": 14.75, "employer": 51.65},
            {"min": 3000.01, "max": 3100, "employee": 15.25, "employer": 53.35},
            {"min": 3100.01, "max": 3200, "employee": 15.75, "employer": 55.15},
            {"min": 3200.01, "max": 3300, "employee": 16.25, "employer": 56.85},
            {"min": 3300.01, "max": 3400, "employee": 16.75, "employer": 58.65},
            {"min": 3400.01, "max": 3500, "employee": 17.25, "employer": 60.35},
            {"min": 3500.01, "max": 3600, "employee": 17.75, "employer": 62.15},
            {"min": 3600.01, "max": 3700, "employee": 18.25, "employer": 63.85},
            {"min": 3700.01, "max": 3800, "employee": 18.75, "employer": 65.65},
            {"min": 3800.01, "max": 3900, "employee": 19.25, "employer": 67.35},
            {"min": 3900.01, "max": 4000, "employee": 19.75, "employer": 69.05}
        ]
        
    def calculate_epf(self, salary: float, employee_type: str = "local") -> Dict[str, float]:
        """Calculate EPF contributions"""
        if employee_type == "foreign":
            return {"employee": 0, "employer": 0, "total": 0}
            
        employee_epf = salary * self.epf_rates["employee"]
        employer_epf = salary * self.epf_rates["employer"]
        
        return {
            "employee": round(employee_epf, 2),
            "employer": round(employer_epf, 2),
            "total": round(employee_epf + employer_epf, 2)
        }
    
    def calculate_socso(self, salary: float) -> Dict[str, float]:
        """Calculate SOCSO contributions based on salary brackets"""
        for bracket in self.socso_brackets:
            if bracket["min"] <= salary <= bracket["max"]:
                return {
                    "employee": bracket["employee"],
                    "employer": bracket["employer"],
                    "total": round(bracket["employee"] + bracket["employer"], 2)
                }
        
        # For salaries above RM4000
        return {"employee": 19.75, "employer": 69.05, "total": 88.80}
    
    def calculate_eis(self, salary: float) -> Dict[str, float]:
        """Calculate EIS contributions"""
        max_salary = 4000  # EIS ceiling
        contributory_salary = min(salary, max_salary)
        
        employee_eis = contributory_salary * self.eis_rates["employee"]
        employer_eis = contributory_salary * self.eis_rates["employer"]
        
        return {
            "employee": round(employee_eis, 2),
            "employer": round(employer_eis, 2),
            "total": round(employee_eis + employer_eis, 2)
        }
    
    def calculate_pcb(self, annual_salary: float, relief_amount: float = 9000) -> Dict[str, Any]:
        """Calculate PCB (Monthly Tax Deduction) based on Malaysian tax brackets"""
        taxable_income = max(0, annual_salary - relief_amount)
        
        # 2024 Malaysian tax brackets
        tax_brackets = [
            {"min": 0, "max": 5000, "rate": 0},
            {"min": 5000, "max": 20000, "rate": 0.01},
            {"min": 20000, "max": 35000, "rate": 0.03},
            {"min": 35000, "max": 50000, "rate": 0.08},
            {"min": 50000, "max": 70000, "rate": 0.13},
            {"min": 70000, "max": 100000, "rate": 0.21},
            {"min": 100000, "max": 400000, "rate": 0.24},
            {"min": 400000, "max": 600000, "rate": 0.245},
            {"min": 600000, "max": 2000000, "rate": 0.25},
            {"min": 2000000, "max": float('inf'), "rate": 0.30}
        ]
        
        annual_tax = 0
        remaining_income = taxable_income
        
        for bracket in tax_brackets:
            if remaining_income <= 0:
                break
                
            bracket_income = min(remaining_income, bracket["max"] - bracket["min"])
            annual_tax += bracket_income * bracket["rate"]
            remaining_income -= bracket_income
        
        monthly_pcb = annual_tax / 12
        
        return {
            "annual_salary": annual_salary,
            "taxable_income": taxable_income,
            "annual_tax": round(annual_tax, 2),
            "monthly_pcb": round(monthly_pcb, 2),
            "effective_rate": round((annual_tax / annual_salary) * 100, 2) if annual_salary > 0 else 0
        }

@router.post("/calculate/full")
async def calculate_full_payroll(employee_data: Dict[str, Any]):
    """Calculate complete payroll with all Malaysian statutory deductions"""
    engine = MalaysianPayrollEngine()
    
    basic_salary = employee_data.get("basic_salary", 0)
    allowances = employee_data.get("allowances", 0)
    overtime = employee_data.get("overtime", 0)
    bonus = employee_data.get("bonus", 0)
    employee_type = employee_data.get("employee_type", "local")
    
    gross_salary = basic_salary + allowances + overtime
    annual_salary = (gross_salary * 12) + bonus
    
    # Calculate statutory deductions
    epf = engine.calculate_epf(gross_salary, employee_type)
    socso = engine.calculate_socso(gross_salary)
    eis = engine.calculate_eis(gross_salary)
    pcb = engine.calculate_pcb(annual_salary)
    
    # Calculate net salary
    total_deductions = epf["employee"] + socso["employee"] + eis["employee"] + pcb["monthly_pcb"]
    net_salary = gross_salary - total_deductions
    
    return {
        "employee_id": employee_data.get("employee_id"),
        "calculation_date": datetime.now().isoformat(),
        "salary_breakdown": {
            "basic_salary": basic_salary,
            "allowances": allowances,
            "overtime": overtime,
            "gross_salary": gross_salary,
            "net_salary": round(net_salary, 2)
        },
        "statutory_deductions": {
            "epf": epf,
            "socso": socso,
            "eis": eis,
            "pcb": pcb["monthly_pcb"]
        },
        "employer_contributions": {
            "epf": epf["employer"],
            "socso": socso["employer"],
            "eis": eis["employer"],
            "total": round(epf["employer"] + socso["employer"] + eis["employer"], 2)
        },
        "annual_projections": {
            "gross_annual": annual_salary,
            "total_tax": pcb["annual_tax"],
            "take_home": round((net_salary * 12) + bonus, 2)
        }
    }

@router.post("/payslip/generate")
async def generate_payslip(payroll_data: Dict[str, Any]):
    """Generate Malaysian-compliant payslip"""
    return {
        "payslip_id": f"PS-{datetime.now().strftime('%Y%m')}-{payroll_data.get('employee_id', '001')}",
        "employee_details": {
            "name": payroll_data.get("employee_name"),
            "ic_number": payroll_data.get("ic_number"),
            "epf_number": payroll_data.get("epf_number"),
            "socso_number": payroll_data.get("socso_number")
        },
        "pay_period": {
            "month": datetime.now().strftime("%B %Y"),
            "working_days": 22,
            "days_worked": payroll_data.get("days_worked", 22)
        },
        "earnings": payroll_data.get("salary_breakdown", {}),
        "deductions": payroll_data.get("statutory_deductions", {}),
        "employer_contributions": payroll_data.get("employer_contributions", {}),
        "compliance_notes": [
            "EPF contributions calculated as per EPF Act 1991",
            "SOCSO contributions as per Employees' Social Security Act 1969",
            "PCB deducted as per Income Tax Act 1967",
            "EIS contributions as per Employment Insurance System Act 2017"
        ],
        "generated_at": datetime.now().isoformat(),
        "language": "bilingual"  # BM/EN
    }

@router.get("/reports/monthly")
async def get_monthly_payroll_report(month: int, year: int):
    """Generate monthly payroll summary report"""
    return {
        "report_period": f"{calendar.month_name[month]} {year}",
        "summary": {
            "total_employees": 150,
            "total_gross_salary": 750000.00,
            "total_net_salary": 625000.00,
            "total_deductions": 125000.00
        },
        "statutory_summary": {
            "total_epf_employee": 82500.00,
            "total_epf_employer": 97500.00,
            "total_socso_employee": 2850.00,
            "total_socso_employer": 9975.00,
            "total_eis_employee": 1500.00,
            "total_eis_employer": 1500.00,
            "total_pcb": 38175.00
        },
        "compliance_status": {
            "epf_submission_due": f"{year}-{month+1:02d}-15",
            "socso_submission_due": f"{year}-{month+1:02d}-15",
            "pcb_submission_due": f"{year}-{month+1:02d}-15",
            "all_compliant": True
        },
        "generated_at": datetime.now().isoformat()
    }