import pytest
from backend.core.models import EPFCalculation, DisputeCase, HRDFCourse
from backend.core.malaysian_compliance import MalaysianCompliance

def test_epf_calculation():
    """Test EPF calculation with standard rates"""
    calc = EPFCalculation(basic_salary=5000)
    result = MalaysianCompliance.calculate_epf(calc)
    
    assert result["employee_share"] == 550.0  # 5000 * 0.11
    assert result["employer_share"] == 650.0  # 5000 * 0.13
    assert result["total"] == 1200.0

def test_socso_calculation():
    """Test SOCSO calculation with salary cap"""
    result = MalaysianCompliance.calculate_socso(5000)
    
    # SOCSO capped at 4000
    assert result["employee_contribution"] == 20.0  # 4000 * 0.005
    assert result["employer_contribution"] == 70.0  # 4000 * 0.0175

def test_hrdf_claim():
    """Test HRDF claim calculation"""
    course = HRDFCourse(code="TEST001", hours=40, provider="Test Provider")
    claimable = MalaysianCompliance.claim_hrdf(course, 5000)
    
    # 40 hours * RM80 = RM3200, but limited by levy balance
    assert claimable == 3200.0

def test_dispute_case_validation():
    """Test Malaysian case ID validation"""
    case = DisputeCase(
        case_id="MYIR-2024-001",
        employee_ic="123456-12-1234",
        dispute_type="Misconduct"
    )
    assert case.case_id == "MYIR-2024-001"
    assert case.employee_ic == "123456-12-1234"