from typing import Annotated
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class DisputeType(str, Enum):
    MISCONDUCT = "Misconduct"
    UNFAIR_DISMISSAL = "UnfairDismissal"
    WAGE_CLAIM = "WageClaim"

class DisputeCase(BaseModel):
    case_id: Annotated[str, Field(pattern=r'^MYIR-\d{4}-\d+$')]
    employee_ic: Annotated[str, Field(pattern=r'^\d{6}-\d{2}-\d{4}$')]
    dispute_type: DisputeType
    resolution_status: bool = False

class PulseSurvey(BaseModel):
    department: str
    engagement_score: Annotated[float, Field(ge=0, le=10)]
    comments: list[str] = []

class HRDFCourse(BaseModel):
    code: str
    hours: float
    provider: str
    claimable_amount: float = 0

class MalaysianResume(BaseModel):
    ic_number: Annotated[str, Field(pattern=r'^\d{6}-\d{2}-\d{4}$')]
    education: list[dict]
    skills: list[str]
    university: str = ""

class EPFCalculation(BaseModel):
    basic_salary: float
    employee_rate: float = 0.11
    employer_rate: float = 0.13