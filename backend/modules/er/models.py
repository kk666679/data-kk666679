from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PulseSurvey(Base):
    __tablename__ = "pulse_surveys"
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    survey_date = Column(DateTime)
    engagement_score = Column(Float)
    sentiment_score = Column(Float)  # AI-analyzed sentiment
    feedback_text = Column(Text)
    department = Column(String(50))
    is_anonymous = Column(Boolean, default=True)

class MisconductCase(Base):
    __tablename__ = "misconduct_cases"
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    case_type = Column(String(50))  # warning, show_cause, suspension
    description = Column(Text)
    action_taken = Column(String(100))
    created_at = Column(DateTime)
    hr_officer_id = Column(Integer, ForeignKey("employees.id"))

class WhistleblowReport(Base):
    __tablename__ = "whistleblow_reports"
    
    id = Column(Integer, primary_key=True)
    report_id = Column(String(20), unique=True)  # Anonymous ID
    category = Column(String(50))  # harassment, corruption, safety
    description = Column(Text)
    status = Column(String(20))  # submitted, investigating, closed
    created_at = Column(DateTime)