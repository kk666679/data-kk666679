from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DisputeCase(Base):
    __tablename__ = "dispute_cases"
    
    id = Column(Integer, primary_key=True)
    case_number = Column(String(50), unique=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    case_type = Column(String(50))  # misconduct, grievance, unfair_dismissal
    status = Column(String(20))  # open, investigating, resolved, escalated
    description = Column(Text)
    created_at = Column(DateTime)
    resolved_at = Column(DateTime, nullable=True)

class CollectiveAgreement(Base):
    __tablename__ = "collective_agreements"
    
    id = Column(Integer, primary_key=True)
    union_name = Column(String(100))
    agreement_title = Column(String(200))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    document_path = Column(String(500))
    renewal_reminder_sent = Column(Boolean, default=False)