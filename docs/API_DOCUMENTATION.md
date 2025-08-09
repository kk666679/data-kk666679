# HRMS Malaysia API Documentation

## Industrial Relations (IR) Module

### Dispute Management
```
POST /api/ir/disputes
GET /api/ir/disputes/{case_id}
PUT /api/ir/disputes/{case_id}/status
```

### Collective Agreements
```
POST /api/ir/agreements
GET /api/ir/agreements/expiring
```

## Employee Relations (ER) Module

### Pulse Surveys
```
POST /api/er/surveys
GET /api/er/surveys/analytics
```

### Misconduct Cases
```
POST /api/er/misconduct
GET /api/er/misconduct/{employee_id}
```

## Learning & Development (L&D) Module

### HRDF Claims
```
POST /api/ld/hrdf-claims
GET /api/ld/hrdf-claims/status/{claim_id}
```

### Training Courses
```
GET /api/ld/courses/recommended/{employee_id}
POST /api/ld/enrollments
```

## Talent Acquisition (TA) Module

### Resume Parsing
```
POST /api/ta/parse-resume
```

### Job Postings
```
POST /api/ta/jobs
GET /api/ta/jobs/{job_id}/candidates
```

### Interview Scheduling
```
POST /api/ta/interviews/schedule
GET /api/ta/interviews/available-slots
```

## Payroll Module

### Malaysian Compliance
```
POST /api/payroll/calculate-statutory
GET /api/payroll/epf-report/{month}
GET /api/payroll/socso-report/{month}
```