from datetime import datetime
from typing import Dict
from .models import DisputeCase, HRDFCourse, EPFCalculation

class MalaysianCompliance:
    
    @staticmethod
    async def auto_fill_pk_form(case: DisputeCase) -> Dict:
        """Auto-generates JTK PK Form for termination notifications"""
        return {
            **case.model_dump(),
            "jtk_reference": f"PK/{datetime.now().year}/{case.case_id.split('-')[-1]}",
            "form_type": "PK_TERMINATION",
            "generated_at": datetime.now().isoformat()
        }
    
    @staticmethod
    def calculate_epf(calculation: EPFCalculation) -> Dict:
        """EPF Calculation with Malaysian rates"""
        employee_share = round(calculation.basic_salary * calculation.employee_rate, 2)
        employer_share = round(calculation.basic_salary * calculation.employer_rate, 2)
        
        return {
            "employee_share": employee_share,
            "employer_share": employer_share,
            "total": round(employee_share + employer_share, 2),
            "salary": calculation.basic_salary
        }
    
    @staticmethod
    def claim_hrdf(course: HRDFCourse, levy_balance: float) -> float:
        """Automates HRDF claim calculations"""
        claimable = min(course.hours * 80, levy_balance)  # MYR 80/hour cap
        return round(claimable, 2)
    
    @staticmethod
    def calculate_socso(basic_salary: float) -> Dict:
        """SOCSO calculation with Malaysian rates"""
        socso_salary = min(basic_salary, 4000)  # SOCSO cap
        employee_rate = 0.005
        employer_rate = 0.0175
        
        return {
            "employee_contribution": round(socso_salary * employee_rate, 2),
            "employer_contribution": round(socso_salary * employer_rate, 2),
            "total_contribution": round(socso_salary * (employee_rate + employer_rate), 2)
        }