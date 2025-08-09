#!/usr/bin/env python3
"""
HRMS Malaysia API Demo Script
Demonstrates modern Python features and Malaysian compliance
"""

import asyncio
from core.models import EPFCalculation, DisputeCase, PulseSurvey, HRDFCourse
from core.malaysian_compliance import MalaysianCompliance
from core.ai_services import MalaysianAIServices

async def demo_malaysian_hrms():
    """Demo of HRMS Malaysia core features"""
    
    print("🇲🇾 HRMS Malaysia - AI-Powered Demo")
    print("=" * 40)
    
    # 1. EPF Calculation
    print("\n1. EPF Calculation:")
    epf_calc = EPFCalculation(basic_salary=4500)
    epf_result = MalaysianCompliance.calculate_epf(epf_calc)
    print(f"   Salary: RM{epf_calc.basic_salary}")
    print(f"   Employee: RM{epf_result['employee_share']}")
    print(f"   Employer: RM{epf_result['employer_share']}")
    
    # 2. SOCSO Calculation
    print("\n2. SOCSO Calculation:")
    socso_result = MalaysianCompliance.calculate_socso(4500)
    print(f"   Employee: RM{socso_result['employee_contribution']}")
    print(f"   Employer: RM{socso_result['employer_contribution']}")
    
    # 3. Dispute Case with Malaysian IC validation
    print("\n3. Industrial Relations - Dispute Case:")
    dispute = DisputeCase(
        case_id="MYIR-2024-001",
        employee_ic="850123-08-1234",
        dispute_type="Misconduct"
    )
    pk_form = await MalaysianCompliance.auto_fill_pk_form(dispute)
    print(f"   Case ID: {dispute.case_id}")
    print(f"   JTK Reference: {pk_form['jtk_reference']}")
    
    # 4. HRDF Claim
    print("\n4. Learning & Development - HRDF Claim:")
    course = HRDFCourse(
        code="HRDF/LEADERSHIP/2024",
        hours=35,
        provider="Malaysian Institute of Management"
    )
    claimable = MalaysianCompliance.claim_hrdf(course, 8000)
    print(f"   Course: {course.code}")
    print(f"   Claimable: RM{claimable}")
    
    # 5. AI Sentiment Analysis
    print("\n5. Employee Relations - AI Sentiment:")
    ai_services = MalaysianAIServices()
    survey = PulseSurvey(
        department="IT",
        engagement_score=7.5,
        comments=["Great work environment", "Good benefits"]
    )
    sentiment = ai_services.analyze_employee_sentiment(survey)
    print(f"   Department: {sentiment['department']}")
    print(f"   Sentiment: {sentiment['sentiment']}")
    
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    asyncio.run(demo_malaysian_hrms())