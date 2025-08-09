from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JobPosting(Base):
    __tablename__ = "job_postings"
    
    id = Column(Integer, primary_key=True)
    job_title = Column(String(100))
    department = Column(String(50))
    location = Column(String(50))  # Klang Valley, Johor, Penang
    salary_min = Column(Float)
    salary_max = Column(Float)
    posted_to_jobstreet = Column(Boolean, default=False)
    posted_to_linkedin = Column(Boolean, default=False)
    posted_to_maukerja = Column(Boolean, default=False)
    created_at = Column(DateTime)

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    university = Column(String(100))  # UM, USM, Taylor's, etc.
    ai_score = Column(Float)  # ML-generated score
    skills_match_score = Column(Float)
    cultural_fit_score = Column(Float)
    bahasa_proficiency = Column(String(20))  # native, fluent, basic
    ethnicity = Column(String(20))  # For diversity tracking
    resume_path = Column(String(500))

class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"))
    interview_date = Column(DateTime)
    interview_type = Column(String(20))  # video, face_to_face
    interviewer_id = Column(Integer, ForeignKey("employees.id"))
    status = Column(String(20))  # scheduled, completed, cancelled
    recording_path = Column(String(500), nullable=True)