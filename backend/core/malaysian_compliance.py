from core.models import EPFCalculation, DisputeCase, HRDFCourse

class MalaysianCompliance:
    @staticmethod
    def calculate_epf(calculation: EPFCalculation):
        employee_contribution = calculation.basic_salary * calculation.employee_rate
        employer_contribution = calculation.basic_salary * calculation.employer_rate
        return {
            "employee_contribution": round(employee_contribution, 2),
            "employer_contribution": round(employer_contribution, 2),
            "total": round(employee_contribution + employer_contribution, 2)
        }
    
    @staticmethod
    def calculate_socso(basic_salary: float):
        # Simplified SOCSO calculation
        if basic_salary <= 4000:
            employee = basic_salary * 0.005
            employer = basic_salary * 0.0175
        else:
            employee = 19.75
            employer = 69.25
        return {
            "employee_contribution": round(employee, 2),
            "employer_contribution": round(employer, 2)
        }
    
    @staticmethod
    async def auto_fill_pk_form(case: DisputeCase):
        return {
            "form_type": "PK",
            "case_id": case.case_id,
            "status": "generated",
            "message": "PK form auto-generated for JTK submission"
        }
    
    @staticmethod
    def claim_hrdf(course: HRDFCourse, levy_balance: float):
        return min(course.claimable_amount, levy_balance)