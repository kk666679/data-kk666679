from typing import Annotated, Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import datetime, date
import uuid

class EmployeeStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive" 
    TERMINATED = "terminated"
    ON_LEAVE = "on_leave"

class Employee(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    employee_id: Annotated[str, Field(pattern=r'^EMP\d{6}$')]
    ic_number: Annotated[str, Field(pattern=r'^\d{6}-\d{2}-\d{4}$')]
    full_name: str
    email: Annotated[str, Field(pattern=r'^[^@]+@[^@]+\.[^@]+$')]
    phone: Annotated[str, Field(pattern=r'^\+60\d{8,10}$')]
    department: str
    position: str
    hire_date: date
    salary: Annotated[float, Field(gt=0)]
    status: EmployeeStatus = EmployeeStatus.ACTIVE
    
    @validator('hire_date')
    def validate_hire_date(cls, v):
        if v > date.today():
            raise ValueError('Hire date cannot be in the future')
        return v

class AttendanceRecord(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    employee_id: str
    check_in: datetime
    check_out: Optional[datetime] = None
    location: str
    work_hours: Optional[float] = None
    overtime_hours: Optional[float] = None
    
    @validator('work_hours', always=True)
    def calculate_work_hours(cls, v, values):
        if 'check_out' in values and values['check_out']:
            delta = values['check_out'] - values['check_in']
            return round(delta.total_seconds() / 3600, 2)
        return v

class LeaveRequest(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    employee_id: str
    leave_type: str  # annual, sick, maternity, emergency
    start_date: date
    end_date: date
    days_requested: int
    reason: str
    status: str = "pending"  # pending, approved, rejected
    approved_by: Optional[str] = None
    
class PayrollRecord(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    employee_id: str
    pay_period: str  # YYYY-MM format
    basic_salary: float
    allowances: float = 0
    overtime_pay: float = 0
    gross_salary: float
    epf_employee: float
    epf_employer: float
    socso_employee: float
    socso_employer: float
    pcb_tax: float
    net_salary: float