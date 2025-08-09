from datetime import datetime
from typing import Dict

class MalaysianPayrollCalculator:
    def __init__(self):
        self.epf_employee_rate = 0.11
        self.epf_employer_rate = 0.12
        self.socso_employee_rate = 0.005
        self.socso_employer_rate = 0.0175
        self.eis_employee_rate = 0.002
        self.eis_employer_rate = 0.002
        
    def calculate_statutory_deductions(self, gross_salary: float) -> Dict:
        """Calculate EPF, SOCSO, EIS deductions"""
        
        # EPF calculation (capped at RM5000)
        epf_salary = min(gross_salary, 5000)
        epf_employee = epf_salary * self.epf_employee_rate
        epf_employer = epf_salary * self.epf_employer_rate
        
        # SOCSO calculation (capped at RM4000)
        socso_salary = min(gross_salary, 4000)
        socso_employee = socso_salary * self.socso_employee_rate
        socso_employer = socso_salary * self.socso_employer_rate
        
        # EIS calculation (capped at RM4000)
        eis_salary = min(gross_salary, 4000)
        eis_employee = eis_salary * self.eis_employee_rate
        eis_employer = eis_salary * self.eis_employer_rate
        
        return {
            "epf_employee": round(epf_employee, 2),
            "epf_employer": round(epf_employer, 2),
            "socso_employee": round(socso_employee, 2),
            "socso_employer": round(socso_employer, 2),
            "eis_employee": round(eis_employee, 2),
            "eis_employer": round(eis_employer, 2),
            "total_employee_deduction": round(epf_employee + socso_employee + eis_employee, 2),
            "total_employer_contribution": round(epf_employer + socso_employer + eis_employer, 2)
        }
    
    def calculate_pcb_tax(self, monthly_salary: float, tax_relief: float = 0) -> float:
        """Simplified PCB calculation"""
        annual_salary = monthly_salary * 12
        taxable_income = annual_salary - tax_relief
        
        if taxable_income <= 5000:
            return 0
        elif taxable_income <= 20000:
            return (taxable_income - 5000) * 0.01 / 12
        elif taxable_income <= 35000:
            return (150 + (taxable_income - 20000) * 0.03) / 12
        else:
            return (600 + (taxable_income - 35000) * 0.08) / 12