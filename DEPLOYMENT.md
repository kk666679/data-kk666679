# HRMS Malaysia v3.0 - Production Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Docker 24.0+ and Docker Compose 2.20+
- 8GB RAM minimum (16GB recommended)
- 50GB disk space
- SSL certificates for production

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/your-org/hrms-malaysia.git
cd hrms-malaysia

# Copy environment template
cp .env.example .env.production

# Update with your values
nano .env.production
```

### 2. SSL Configuration
```bash
# Create SSL directory
mkdir -p nginx/ssl

# Add your SSL certificates
cp your-cert.pem nginx/ssl/cert.pem
cp your-key.pem nginx/ssl/key.pem
```

### 3. Deploy
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Start all services
./scripts/start_services.sh
```

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │    │    Frontend     │    │    Backend      │
│  Load Balancer  │────│   React App     │────│   FastAPI       │
│   SSL/Security  │    │   (Port 3000)   │    │   (Port 8000)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐    ┌─────────────────┐
         │              │   AI Services   │    │   PostgreSQL    │
         └──────────────│  (Port 8001)    │────│   Database      │
                        │  ML Models      │    │   (Port 5432)   │
                        └─────────────────┘    └─────────────────┘
                                 │                       │
                        ┌─────────────────┐    ┌─────────────────┐
                        │     Redis       │    │   Monitoring    │
                        │   Cache/Queue   │    │ Prometheus/Graf │
                        │   (Port 6379)   │    │ (Ports 9090/3001)│
                        └─────────────────┘    └─────────────────┘
```

## 🔧 Configuration

### Environment Variables (.env.production)
```bash
# Database
DATABASE_URL=postgresql://hrms_user:${POSTGRES_PASSWORD}@postgres:5432/hrms_db
POSTGRES_PASSWORD=your-secure-password

# Redis
REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379
REDIS_PASSWORD=your-redis-password

# Security
SECRET_KEY=your-32-char-secret-key
JWT_SECRET_KEY=your-jwt-secret-key

# Malaysian APIs
EPF_API_KEY=your-epf-api-key
SOCSO_API_KEY=your-socso-api-key
HRDF_API_KEY=your-hrdf-api-key
LHDN_API_KEY=your-lhdn-api-key

# AI Services
OPENAI_API_KEY=your-openai-key
HUGGINGFACE_API_KEY=your-hf-key
```

## 📊 Monitoring & Health Checks

### Access Points
- **Application**: https://your-domain.com
- **API Documentation**: https://your-domain.com/docs
- **Prometheus**: http://your-domain.com:9090
- **Grafana**: http://your-domain.com:3001

### Health Endpoints
```bash
# Backend health
curl https://your-domain.com/health

# AI services health
curl http://localhost:8001/health

# Database health
docker-compose exec postgres pg_isready
```

## 🇲🇾 Malaysian Compliance Features

### EPF Integration
- Automatic rate calculations (11% employee, 13% employer)
- Monthly contribution reports
- API integration with MyEPF portal

### SOCSO Integration
- Automatic premium calculations
- Injury/disability coverage tracking
- Integration with MySocso portal

### HRDF Claims
- Training course eligibility checking
- Automatic claim submissions
- Levy balance tracking

### Tax Compliance
- PCB (Pay As You Earn) calculations
- EA Form generation
- LHDN integration

## 🔒 Security Features

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (RBAC)
- Multi-factor authentication (MFA)
- Session management

### Data Protection
- AES-256 encryption at rest
- TLS 1.3 for data in transit
- PDPA 2010 compliance
- Audit logging

### API Security
- Rate limiting (100 req/min)
- CORS protection
- Input validation
- SQL injection prevention

## 🤖 AI Features

### Resume Screening
- Malaysian university recognition
- Local skills extraction
- Cultural fit assessment
- Bias detection

### Sentiment Analysis
- Employee feedback analysis
- Multi-language support (BM/EN/ZH)
- Risk prediction
- Intervention recommendations

### Predictive Analytics
- Attrition prediction
- Performance forecasting
- Workforce planning
- Salary benchmarking

## 📱 Mobile App

### Features
- Employee self-service
- Leave applications
- Payslip access
- Training enrollment
- Biometric authentication

### Deployment
```bash
# Build Android APK
cd mobile
flutter build apk --release

# Build iOS IPA
flutter build ios --release
```

## 🔧 Maintenance

### Database Backup
```bash
# Automated daily backups
docker-compose exec postgres pg_dump -U hrms_user hrms_db > backup_$(date +%Y%m%d).sql
```

### Log Management
```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f ai-services

# Log rotation (configured in docker-compose.yml)
```

### Updates
```bash
# Pull latest updates
git pull origin main

# Rebuild and restart
docker-compose build --no-cache
docker-compose up -d
```

## 🚨 Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check database status
docker-compose exec postgres pg_isready -U hrms_user

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

#### AI Services Not Loading
```bash
# Check AI service logs
docker-compose logs ai-services

# Restart AI services
docker-compose restart ai-services
```

#### High Memory Usage
```bash
# Monitor resource usage
docker stats

# Adjust memory limits in docker-compose.yml
```

### Performance Optimization

#### Database Optimization
- Enable connection pooling
- Add database indexes
- Regular VACUUM operations

#### Redis Optimization
- Configure memory policies
- Enable persistence
- Monitor key expiration

#### AI Model Optimization
- Use model quantization
- Implement model caching
- Batch processing

## 📞 Support

### Documentation
- API Documentation: `/docs`
- User Manual: `/docs/user-guide`
- Developer Guide: `/docs/dev-guide`

### Contact
- Technical Support: support@hrms-malaysia.com
- Sales: sales@hrms-malaysia.com
- Emergency: +60-3-XXXX-XXXX

## 📋 Compliance Checklist

- [ ] EPF registration completed
- [ ] SOCSO integration tested
- [ ] HRDF account linked
- [ ] LHDN API configured
- [ ] PDPA compliance verified
- [ ] Security audit completed
- [ ] Backup procedures tested
- [ ] Monitoring alerts configured
- [ ] SSL certificates installed
- [ ] Performance benchmarks met

## 🎯 Next Steps

1. **Week 1**: Basic deployment and testing
2. **Week 2**: Malaysian compliance integration
3. **Week 3**: AI features configuration
4. **Week 4**: Mobile app deployment
5. **Month 2**: Advanced features and optimization

---

**HRMS Malaysia v3.0** - Empowering Malaysian businesses with AI-driven HR management 🇲🇾