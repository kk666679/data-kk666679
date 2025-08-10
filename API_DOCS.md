# HRMS Malaysia API Documentation

## Dashboard Endpoints

| Endpoint | Method | Parameters | Description | Compliance Check |
|----------|--------|------------|-------------|------------------|
| `/api/dashboard` | GET | None | Unified dashboard data | All modules ✅ |
| `/api/dashboard/ir` | GET | `region=KL/Johor` | Industrial Relations metrics | Employment Act 1955 ✅ |
| `/api/dashboard/er` | GET | `lang=BM/English` | Employee Relations sentiment | PDPA 2010 ✅ |
| `/api/dashboard/ta` | GET | `diversity=true` | Talent Acquisition funnel | Anti-Discrimination ✅ |
| `/api/dashboard/ld` | GET | `hrdf=true` | Learning & Development claims | HRDF Compliance ✅ |
| `/api/dashboard/payroll` | GET | `statutory=true` | Payroll compliance status | EPF/SOCSO/EIS ✅ |

## Module-Specific APIs

### Industrial Relations (IR)
- `POST /api/ir/dispute/predict` - AI case resolution prediction
- `GET /api/ir/collective-agreements` - Active union agreements
- `POST /api/ir/generate-form32` - Auto-generate Industrial Court forms

### Employee Relations (ER)
- `POST /api/er/sentiment/analyze` - Malaysian sentiment analysis
- `POST /api/er/burnout/predict` - Cultural burnout prediction
- `POST /api/er/whistleblowing/submit` - Anonymous reporting (PDPA compliant)

### Talent Acquisition (TA)
- `POST /api/ta/resume/score` - Malaysian resume scoring
- `POST /api/ta/job-posting/bias-check` - Discriminatory language detection
- `GET /api/ta/candidates/diversity-report` - Hiring diversity analytics

### Learning & Development (L&D)
- `POST /api/ld/hrdf/claim` - HRDF claim processing
- `POST /api/ld/learning-path/generate` - Personalized learning paths
- `GET /api/ld/courses/library` - Multi-language course catalog

### Payroll
- `POST /api/payroll/calculate/full` - Complete Malaysian payroll calculation
- `POST /api/payroll/payslip/generate` - Bilingual payslip generation
- `GET /api/payroll/reports/monthly` - Statutory compliance reports

## Real-time Features

### WebSocket Endpoints
- `ws://localhost:8000/ws/dashboard` - Real-time dashboard updates
- `ws://localhost:8000/ws/ta/candidates` - Live recruitment pipeline
- `ws://localhost:8000/ws/er/sentiment` - Employee sentiment monitoring

### Authentication
All endpoints require JWT authentication:
```bash
curl -H "Authorization: Bearer <jwt_token>" \
     -X GET http://localhost:8000/api/dashboard
```

## Response Format
```json
{
  "status": "success",
  "data": { ... },
  "timestamp": "2024-01-15T10:30:00Z",
  "compliance": {
    "malaysian_law": true,
    "pdpa_compliant": true
  }
}
```

## Error Codes
- `400` - Bad Request (Invalid parameters)
- `401` - Unauthorized (Invalid JWT token)
- `403` - Forbidden (Insufficient permissions)
- `404` - Not Found (Resource not found)
- `500` - Internal Server Error

## Rate Limiting
- Dashboard endpoints: 100 requests/minute
- Calculation endpoints: 50 requests/minute
- File upload endpoints: 10 requests/minute