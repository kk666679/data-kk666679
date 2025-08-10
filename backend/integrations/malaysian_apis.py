import httpx
import asyncio
from typing import Dict, Optional
from datetime import datetime
import os

class MalaysianAPIIntegration:
    def __init__(self):
        self.epf_api_key = os.getenv("EPF_API_KEY")
        self.socso_api_key = os.getenv("SOCSO_API_KEY")
        self.hrdf_api_key = os.getenv("HRDF_API_KEY")
        self.lhdn_api_key = os.getenv("LHDN_API_KEY")
        
        self.base_urls = {
            "epf": "https://api.kwsp.gov.my/v1",
            "socso": "https://api.perkeso.gov.my/v1", 
            "hrdf": "https://api.hrdf.com.my/v1",
            "lhdn": "https://api.hasil.gov.my/v1"
        }

    async def submit_epf_contribution(self, employee_data: Dict) -> Dict:
        """Submit EPF contribution to MyEPF portal"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_urls['epf']}/contributions",
                headers={"Authorization": f"Bearer {self.epf_api_key}"},
                json={
                    "employee_id": employee_data["ic_number"],
                    "employer_id": employee_data["employer_id"],
                    "contribution_month": datetime.now().strftime("%Y-%m"),
                    "employee_contribution": employee_data["epf_employee"],
                    "employer_contribution": employee_data["epf_employer"]
                }
            )
            return response.json()

    async def submit_socso_premium(self, employee_data: Dict) -> Dict:
        """Submit SOCSO premium to MySocso portal"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_urls['socso']}/premiums",
                headers={"Authorization": f"Bearer {self.socso_api_key}"},
                json={
                    "employee_ic": employee_data["ic_number"],
                    "employer_code": employee_data["employer_code"],
                    "premium_amount": employee_data["socso_premium"],
                    "coverage_period": datetime.now().strftime("%Y-%m")
                }
            )
            return response.json()

    async def submit_hrdf_claim(self, training_data: Dict) -> Dict:
        """Submit HRDF training claim"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_urls['hrdf']}/claims",
                headers={"Authorization": f"Bearer {self.hrdf_api_key}"},
                json={
                    "employer_id": training_data["employer_id"],
                    "course_code": training_data["course_code"],
                    "training_hours": training_data["hours"],
                    "claim_amount": training_data["claimable_amount"],
                    "participants": training_data["participants"]
                }
            )
            return response.json()

    async def generate_ea_form(self, employee_data: Dict) -> Dict:
        """Generate EA form via LHDN API"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_urls['lhdn']}/ea-form",
                headers={"Authorization": f"Bearer {self.lhdn_api_key}"},
                json={
                    "employee_ic": employee_data["ic_number"],
                    "employer_tin": employee_data["employer_tin"],
                    "annual_salary": employee_data["annual_salary"],
                    "tax_deducted": employee_data["pcb_deducted"],
                    "year": datetime.now().year
                }
            )
            return response.json()