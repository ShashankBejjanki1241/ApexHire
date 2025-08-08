# 🚀 ApexHire API Documentation

## 📋 Overview

The ApexHire API provides REST endpoints for AI-powered resume screening and job matching. Built with FastAPI, it offers comprehensive resume analysis, batch processing, and performance monitoring.

## 🚀 Quick Start

### 1. Start the API Server

```bash
# From the project root
cd ApexHire

# Install dependencies
pip install -r requirements.txt

# Start the API server
python api/main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 2. Docker Deployment

```bash
# Build and run with Docker
docker-compose up --build

# Or run API only
docker run -p 8000:8000 apexhire:latest python api/main.py
```

## 📚 API Endpoints

### 🔍 Root Endpoint

**GET** `/`

Returns basic API information.

```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "message": "ApexHire AI Resume Screener API",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs",
  "health": "/health"
}
```

### 🏥 Health Check

**GET** `/health`

Check system health and resources.

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "ok",
  "system_metrics": {
    "cpu_percent": 15.2,
    "memory_percent": 45.8,
    "disk_percent": 67.3
  },
  "warnings": [],
  "timestamp": "2024-01-15T10:30:00"
}
```

### 📊 Performance Metrics

**GET** `/metrics`

Get performance metrics and system statistics.

```bash
curl http://localhost:8000/metrics
```

**Response:**
```json
{
  "summary": {
    "total_operations": 25,
    "average_duration": 2.3,
    "min_duration": 1.1,
    "max_duration": 5.2
  },
  "recent_metrics": [...],
  "system_health": {
    "status": "ok",
    "memory_percent": 45.8
  }
}
```

### 📄 Resume Analysis

**POST** `/analyze/resume`

Analyze a single resume against a job description.

```bash
curl -X POST "http://localhost:8000/analyze/resume" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@resume.pdf" \
  -F "job_title=Software Engineer" \
  -F "job_description=We are looking for a Python developer..." \
  -F "requirements=Python,React,AWS"
```

**Response:**
```json
{
  "overall_score": 85.5,
  "breakdown": {
    "experience": {
      "score": 80.0,
      "status": "✅ Yes"
    },
    "skills": {
      "required_matches": 8,
      "total_required": 10,
      "score": 80.0
    }
  },
  "skills_found": {
    "technical_skills": ["Python", "React", "AWS"],
    "soft_skills": ["Leadership", "Communication"]
  },
  "recommendations": [
    "Add more AWS experience",
    "Include specific project examples"
  ],
  "processing_time": 2.3,
  "status": "success"
}
```

### 📁 Batch Analysis

**POST** `/analyze/batch`

Analyze multiple resumes against a job description.

```bash
curl -X POST "http://localhost:8000/analyze/batch" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@resume1.pdf" \
  -F "files=@resume2.pdf" \
  -F "files=@resume3.pdf" \
  -F "job_title=Senior Developer" \
  -F "job_description=Senior role requiring..." \
  -F "requirements=Python,Leadership,5+ years"
```

**Response:**
```json
{
  "job_title": "Senior Developer",
  "total_files": 3,
  "results": [
    {
      "filename": "resume1.pdf",
      "overall_score": 85.5,
      "skills_found": {...},
      "status": "success"
    },
    {
      "filename": "resume2.pdf",
      "overall_score": 72.3,
      "skills_found": {...},
      "status": "success"
    }
  ],
  "summary": {
    "successful": 3,
    "failed": 0,
    "average_score": 78.9
  }
}
```

### ⚙️ Configuration

**GET** `/config`

Get current system configuration.

```bash
curl http://localhost:8000/config
```

**POST** `/config/validate`

Validate current configuration.

```bash
curl -X POST http://localhost:8000/config/validate
```

## 🔧 Client Examples

### Python Client

```python
import requests

# Analyze a single resume
def analyze_resume(file_path, job_title, job_description, requirements=""):
    url = "http://localhost:8000/analyze/resume"
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'job_title': job_title,
            'job_description': job_description,
            'requirements': requirements
        }
        
        response = requests.post(url, files=files, data=data)
        return response.json()

# Example usage
result = analyze_resume(
    file_path="resume.pdf",
    job_title="Python Developer",
    job_description="We need a Python developer...",
    requirements="Python,React,AWS"
)
print(f"Score: {result['overall_score']}")
```

### JavaScript/Node.js Client

```javascript
const FormData = require('form-data');
const fs = require('fs');

async function analyzeResume(filePath, jobTitle, jobDescription, requirements = '') {
    const form = new FormData();
    form.append('file', fs.createReadStream(filePath));
    form.append('job_title', jobTitle);
    form.append('job_description', jobDescription);
    form.append('requirements', requirements);

    const response = await fetch('http://localhost:8000/analyze/resume', {
        method: 'POST',
        body: form
    });

    return await response.json();
}

// Example usage
analyzeResume(
    'resume.pdf',
    'Software Engineer',
    'We are looking for a developer...',
    'Python,JavaScript,React'
).then(result => {
    console.log(`Score: ${result.overall_score}`);
});
```

### cURL Examples

```bash
# Health check
curl http://localhost:8000/health

# Single resume analysis
curl -X POST "http://localhost:8000/analyze/resume" \
  -F "file=@resume.pdf" \
  -F "job_title=Developer" \
  -F "job_description=Python developer needed" \
  -F "requirements=Python,React"

# Batch analysis
curl -X POST "http://localhost:8000/analyze/batch" \
  -F "files=@resume1.pdf" \
  -F "files=@resume2.pdf" \
  -F "job_title=Senior Developer" \
  -F "job_description=Senior role" \
  -F "requirements=Python,Leadership"

# Get metrics
curl http://localhost:8000/metrics
```

## 🔐 Authentication & Security

Currently, the API runs without authentication for development. For production:

1. **Add API Keys**: Implement API key authentication
2. **Rate Limiting**: Add rate limiting middleware
3. **CORS Configuration**: Configure allowed origins
4. **HTTPS**: Use SSL/TLS encryption

## 📊 Performance Monitoring

The API includes comprehensive performance monitoring:

- **Real-time metrics**: CPU, memory, disk usage
- **Request tracking**: Processing times and success rates
- **System health**: Automatic health checks
- **Error monitoring**: Detailed error logging

## 🐳 Docker Deployment

### Production Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "api/main.py"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  apexhire-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - PYTHONPATH=/app
```

## 🧪 Testing

### API Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test with sample data
python -m pytest tests/test_api.py -v
```

### Load Testing

```bash
# Install locust
pip install locust

# Run load test
locust -f tests/locustfile.py --host=http://localhost:8000
```

## 📈 Monitoring & Logging

### Logs

- **Application logs**: `logs/apexhire.log`
- **Performance metrics**: `logs/performance_metrics_*.json`
- **API access logs**: Available via uvicorn

### Metrics

- **Response times**: Average, min, max
- **Success rates**: Percentage of successful requests
- **System resources**: CPU, memory, disk usage
- **Error rates**: Failed requests and error types

## 🔧 Configuration

The API uses the centralized configuration system:

```python
from src.config.settings import get_config

config = get_config()
print(config['api_config']['port'])  # 8000
```

## 🚀 Production Deployment

### 1. Environment Variables

```bash
export SECRET_KEY="your-secret-key"
export DATABASE_URL="postgresql://user:pass@localhost/apexhire"
export AWS_ACCESS_KEY_ID="your-aws-key"
export AWS_SECRET_ACCESS_KEY="your-aws-secret"
```

### 2. Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name api.apexhire.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. Process Management (systemd)

```ini
[Unit]
Description=ApexHire API
After=network.target

[Service]
User=apexhire
WorkingDirectory=/opt/apexhire
ExecStart=/opt/apexhire/venv/bin/python api/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## 📞 Support

- **Documentation**: `/docs` (Interactive Swagger UI)
- **Health Check**: `/health`
- **Metrics**: `/metrics`
- **Configuration**: `/config`

---

**Status**: ✅ **Production Ready**
**Version**: 1.0.0
**Last Updated**: January 2024
