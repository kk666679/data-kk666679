from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HRDFClaim(Base):
    __tablename__ = "hrdf_claims"
    
    id = Column(Integer, primary_key=True)
    claim_number = Column(String(50), unique=True)
    course_id = Column(Integer, ForeignKey("training_courses.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    claim_amount = Column(Float)
    status = Column(String(20))  # submitted, approved, rejected, paid
    submitted_date = Column(DateTime)
    approved_date = Column(DateTime, nullable=True)

class TrainingCourse(Base):
    __tablename__ = "training_courses"
    
    id = Column(Integer, primary_key=True)
    course_name = Column(String(200))
    provider = Column(String(100))
    duration_hours = Column(Integer)
    cost = Column(Float)
    is_hrdf_claimable = Column(Boolean, default=False)
    category = Column(String(50))  # safety, leadership, technical
    language = Column(String(10))  # BM, EN, ZH

class Certification(Base):
    __tablename__ = "certifications"
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    cert_name = Column(String(100))
    cert_body = Column(String(100))  # NIOSH, CIDB, etc.
    issue_date = Column(DateTime)
    expiry_date = Column(DateTime)
    reminder_sent = Column(Boolean, default=False)