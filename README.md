# Complete Human Resource Management System (HRMS) for Malaysian Businesses

![HRMS Dashboard](https://img.shields.io/badge/Dashboard-Live-brightgreen)
![API Status](https://img.shields.io/badge/API-Operational-blue)
![Compliance](https://img.shields.io/badge/Malaysian%20Compliance-100%25-success)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 20+](https://img.shields.io/badge/node.js-20+-green.svg)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/docker-24.0+-blue.svg)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3+-blue.svg)](https://reactjs.org/)
[![Flutter](https://img.shields.io/badge/Flutter-3.24+-blue.svg)](https://flutter.dev/)
[![AI Powered](https://img.shields.io/badge/AI-Powered-purple.svg)](https://openai.com/)
[![Malaysia Ready](https://img.shields.io/badge/Malaysia-Ready-red.svg)](https://www.malaysia.gov.my/)

An AI-powered Human Resource Management System tailored for Malaysian businesses with full compliance to local labor laws and regulations.

## **Table of Contents**
1. **Introduction**
2. **System Overview**
3. **Key Features**
4. **Technology Stack**
5. **Modules & Functionalities**
6. **Compliance & Localization**
7. **AI & Automation**
8. **Deployment Options**
9. **Security & Data Protection**
10. **Integration Capabilities**
11. **User Roles & Permissions**
12. **Reporting & Analytics**
13. **Mobile & Web Access**
14. **Support & Maintenance**
15. **Pricing & Licensing**
16. **Roadmap & Future Enhancements**

---

## **1. Introduction**
A **Human Resource Management System (HRMS)** is a comprehensive software solution designed to streamline HR operations, enhance employee engagement, and ensure compliance with Malaysian labor laws. This document provides a detailed overview of an **AI-powered HRMS** tailored for Malaysian businesses, incorporating **NLP, Multi-Agent AI, and Automation** to optimize HR workflows.

---

## **2. System Overview**
### **Core Objectives**
- **Automate** payroll, attendance, and recruitment.
- **Ensure compliance** with **Malaysian labor laws (Employment Act 1955, EPF, SOCSO, HRDF, etc.)**.
- **Enhance employee experience** with self-service portals.
- **Leverage AI** for resume screening, sentiment analysis, and workforce planning.
- **Multi-language support** (Bahasa Malaysia, English, Mandarin).

### **Target Users**
- **HR Departments** (Payroll, Recruitment, Compliance)
- **Employees** (Self-service leave, claims, training)
- **Management** (Workforce analytics, decision-making)

---

## **3. Key Features**
| **Category** | **Features** |
|-------------|-------------|
| **Recruitment** | AI resume screening, interview scheduling, candidate scoring |
| **Payroll** | Auto EPF/SOCSO/PCB calculations, payslip generation |
| **Attendance** | Biometric/Facial recognition, shift management |
| **Leave Management** | Automated approvals, encashment, carry-forward |
| **Performance** | KPI tracking, 360° feedback, AI-driven insights |
| **Training** | HRDF-claimable courses, skill gap analysis |
| **Compliance** | Real-time law updates, audit trails |
| **Employee Self-Service** | Mobile app for claims, leave, payslips |

---

## **4. Technology Stack**
| **Layer** | **Technology** |
|-----------|--------------|
| **Frontend** | React.js, Flutter (Mobile) |
| **Backend** | Node.js, FastAPI (Python) |
| **Database** | PostgreSQL (Relational), MongoDB (NoSQL) |
| **AI/ML** | TensorFlow, spaCy (NLP), LangChain (Agents) |
| **Cloud** | AWS Malaysia / On-Premise |
| **Security** | AES-256 Encryption, JWT Authentication |

---

## **5. Core Modules & Functionalities**

### **A. Industrial Relations (IR) Module**
*Compliance with Malaysian Labor Laws*

**Key Features:**
- **Dispute Resolution Tracker**
  - Case management for misconduct, grievances, and unfair dismissal
  - Industrial Court case references (Malaysia-specific precedents)
- **Collective Agreement (CA) Management**
  - Digital storage of union agreements
  - Automated reminders for renewal dates
- **Strike & Work Stoppage Alerts**
  - Early warning system using sentiment analysis
- **Compliance Checklists**
  - Employment Act 1955, Trade Unions Act 1959, IRA 1967
- **Reporting for Ministry of Human Resources (KESU)**
  - Auto-generate Form PK for termination notifications

### **B. Employee Relations (ER) Module**
*Workplace Harmony & Engagement*

**Key Features:**
- **Employee Pulse Surveys**
  - AI-driven sentiment analysis (supports Bahasa Malaysia dialects)
  - Anonymous feedback with heat maps (by department/location)
- **Misconduct & Warning System**
  - Digital show-cause letters with audit trails
  - Progressive discipline workflows
- **Whistleblowing Portal**
  - Secure, anonymous reporting (PDPA-compliant)
- **Employee Recognition**
  - Peer-to-peer awards (linked to performance metrics)
- **Industrial Harmony Index**
  - Predictive analytics for conflict risk (ethnicity/language factors)

### **C. Learning & Development (L&D) Module**
*HRDF-Claimable Training*

**Key Features:**
- **Automated HRDF Claims**
  - Direct submission to HRDC portal
  - Track claim status (approved/rejected)
- **Personalized Learning Paths**
  - AI recommends courses based on:
    - Skill gaps
    - Career progression plans
    - Compliance requirements (e.g., OSHA, DOSH)
- **Microlearning Library**
  - Bite-sized courses in BM/English (e.g., "3-min Safety Briefings")
- **Certification Tracking**
  - Auto-alerts for expiring licenses (e.g., NIOSH, CIDB)
- **Virtual Instructor-Led Training (VILT)**
  - Integrates with Zoom/Teams (attendance auto-sync)

### **D. Talent Acquisition (TA) Module**
*AI-Driven Recruitment*

**Key Features:**
- **Malaysia-Optimized Resume Parser**
  - Recognizes local institutions (e.g., UM, USM, Taylor's)
  - Extracts EPF/SOCSO history (with candidate consent)
- **Automated Job Posting**
  - Publishes to JobStreet, LinkedIn, MauKerja
  - AI suggests salary benchmarks (by Klang Valley/Johor/Penang rates)
- **Interview Coordination**
  - Chatbot schedules slots (avoiding prayer times/Raya holidays)
  - Video interview recording (PDPA-compliant storage)
- **Candidate Scoring**
  - Machine Learning ranks applicants based on:
    - Skills match
    - Cultural fit (e.g., Bahasa proficiency)
    - Diversity metrics (Bumiputera/non-Bumiputera ratios)
- **Onboarding Workflows**
  - Digital signing of offer letters
  - Auto-assign mandatory trainings (e.g., Sexual Harassment Policy)

### **E. Payroll & Compliance**
- **Auto EPF/SOCSO/HRDF calculations**
- **PCB (MTD) & EIS deductions**
- **EA Form & CP8D generation**

### **F. Attendance & Shift Management**
- **Biometric/Facial Recognition**
- **Geofencing for remote workers**
- **Overtime & shift rotation rules**

### **G. Performance & Appraisal**
- **OKR & KPI tracking**
- **AI-based performance predictions**
- **360° feedback system**

---

## **6. Compliance & Localization**
### **Malaysia-Specific Features**
✅ **Bahasa Malaysia Support** (NLP for local dialects)  
✅ **Employment Act 1955 Compliance** (Probation, termination rules)  
✅ **EPF/SOCSO/HRDF Auto-Filing**  
✅ **Industrial Court Case Database** (For dispute references)  

---

## **7. AI & Automation**
### **AI-Powered HR Assistants**
| **Agent** | **Function** |
|-----------|-------------|
| **RecruiterAI** | Smart candidate matching |
| **PayrollBot** | Auto tax & statutory compliance |
| **EngageX** | Employee sentiment monitoring |
| **ComplianceGuard** | Real-time labor law updates |

### **NLP Applications**
- **Resume Screening** (Local universities, certifications)
- **Employee Feedback Analysis** (Detect burnout, dissatisfaction)
- **CikguHR Chatbot** (HR Virtual Assistant in BM/English/Mandarin)
- **Bias Detection** (Flags discriminatory language in job ads)
- **Attrition Predictor** (Identifies flight risks using tenure, engagement, market trends)

---

## **8. Deployment Options**
| **Option** | **Details** |
|------------|------------|
| **Cloud (AWS Malaysia)** | Fully managed, automatic updates |
| **On-Premise** | Self-hosted, custom security policies |
| **Hybrid** | Critical data on-premise, AI on cloud |

---

## **9. Security & Data Protection**
- **GDPR & Malaysia PDPA 2010 Compliance**
- **Role-Based Access Control (RBAC)**
- **Biometric Authentication**
- **Audit Logs for All Transactions**

---

## **10. Integration Capabilities**
- **ERP Systems** (SAP, Oracle)
- **Accounting Software** (AutoCount, SQL Accounting)
- **Job Portals** (JobStreet, MauKerja)
- **Government Portals** (MyEPF, MySOCSO)

---

## **11. User Roles & Permissions**
| **Role** | **Access Level** |
|----------|-----------------|
| **HR Admin** | Full system control |
| **Payroll Officer** | Payroll processing only |
| **Employee** | Self-service portal |
| **Manager** | Team attendance, performance |

---

## **12. Reporting & Analytics**
📊 **Real-time HR Dashboards**  
📈 **Workforce Forecasting**  
📉 **Turnover Risk Analysis**  
📋 **Customizable Reports (Excel, PDF)**  

---

## **13. Mobile & Web Access**
📱 **Mobile App (iOS & Android)** Features:
- **Payslips & Tax Documents**
- **Leave Application**
- **Expense Claims**
- **Training Enrollment**

---

## **14. Support & Maintenance**
🛠 **24/5 Helpdesk (Malaysia-based)**  
🔧 **Automatic Compliance Updates**  
📅 **Dedicated Account Manager**  

---

## **Module Integration Matrix**
| **Module** | **Linked To** | **Example Workflow** |
|------------|--------------|----------------------|
| **IR** | Payroll | Terminated employee's final settlement auto-calculated |
| **ER** | Performance | Poor engagement triggers PIP (Performance Improvement Plan) |
| **L&D** | Career Progression | Completing "Leadership 101" unlocks promotion eligibility |
| **TA** | Onboarding | New hire's data flows to EPF/SOCSO registration |

## **15. Pricing & Licensing**

### **Core System**
| **Plan** | **Features** | **Price (MYR)** |
|----------|-------------|-----------------|
| **Starter** | Basic HR & Payroll | RM 299/month |
| **Professional** | AI Recruitment & Analytics | RM 799/month |
| **Enterprise** | Full AI + Multi-Agent HR | Custom Pricing |

### **Module Pricing**
| **Module** | **Starter (MYR)** | **Enterprise (MYR)** |
|------------|-----------------|---------------------|
| **IR** | 200/month | Custom |
| **ER** | 150/month | Custom |
| **L&D** | 300/month (HRDF-claimable) | Custom |
| **TA** | 250/month | Custom |

💡 **HRDF Claimable** (For training modules)
🎁 **Special Offer:** Free 1-hour consultation with Malaysian labor lawyer for annual subscriptions  

---

## **16. Roadmap & Future Enhancements**
- **Q3 2024:** AI-driven succession planning  
- **Q4 2024:** Blockchain for secure document verification  
- **Q1 2025:** Integration with MyDigital ID  

---

### **Why Choose This HRMS?**
✔ **100% Malaysia-Compliant**  
✔ **AI-Powered Automation**  
✔ **Multi-Language Support (BM, English, Mandarin)**  
✔ **Seamless Government Reporting (EPF, SOCSO, LHDN)**  

📞 **Contact Us:**  
📧 sales@xxx.xx.my  
🌐 [www.xxx.xx.my](https://www.xxx.xx.my)  

---

This **Complete HRMS Solution** is designed to **simplify HR tasks, reduce compliance risks, and enhance workforce productivity** for Malaysian businesses of all sizes. 🚀

---

## **Quick Start**

### **Prerequisites**
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- 8GB RAM (for AI models)

### **Installation**

```bash
# Clone repository
git clone https://github.com/your-org/hrms-malaysia.git
cd hrms-malaysia

# Start all services
./scripts/start_services.sh

# Or manual setup
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### **Access Points**
- **API**: http://localhost:8000
- **Dashboard**: http://localhost:8501
- **AI Interface**: http://localhost:7860
- **Monitoring**: http://localhost:9090

### **Environment Variables**
```bash
# Create .env file
DATABASE_URL=postgresql://user:pass@localhost:5432/hrms
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
EPF_API_KEY=your-epf-api-key
SOCSO_API_KEY=your-socso-api-key
```

---

## **Project Structure**
```
hrms-malaysia/
├── backend/           # FastAPI backend
├── frontend/          # React.js frontend
├── mobile/            # Flutter mobile app
├── ai-services/       # AI/ML microservices
├── docs/              # Documentation
├── scripts/           # Deployment scripts
└── tests/             # Test suites
```

---

## **Contributing**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## **License**
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.