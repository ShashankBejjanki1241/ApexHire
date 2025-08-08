# 📁 ApexHire Project Structure

## 🏗️ **Organized Project Layout**

```
ApexHire/
├── 📁 src/                          # Core application source code
│   ├── main_pipeline.py             # Main orchestration logic
│   ├── parser.py                    # Resume file parsing
│   ├── preprocess.py                # Text preprocessing
│   ├── scorer.py                    # Resume scoring algorithms
│   ├── skills_extractor.py          # Skill extraction logic
│   ├── resume_analyzer.py           # Resume analysis engine
│   ├── performance_monitor.py       # Performance monitoring
│   └── utils.py                     # Utility functions
│
├── 📁 api/                          # FastAPI REST API
│   └── main.py                      # API endpoints and logic
│
├── 📁 app/                          # Streamlit web application
│   ├── main.py                      # Web interface
│   └── components/                  # UI components
│
├── 📁 config/                       # Configuration files
│   └── settings.py                  # Centralized configuration
│
├── 📁 docker/                       # Docker configuration
│   ├── Dockerfile                   # Container definition
│   └── docker-compose.yml           # Multi-service setup
│
├── 📁 deployment/                   # Deployment scripts
│   └── deploy.sh                    # Deployment automation
│
├── 📁 docs/                         # Documentation
│   ├── 📁 api/                      # API documentation
│   │   ├── README.md                # API usage guide
│   │   └── API_SUMMARY.md           # API implementation summary
│   ├── 📁 deployment/               # Deployment guides
│   ├── 📁 development/              # Development guides
│   │   └── IMPROVEMENTS.md          # Development improvements
│   ├── USER_GUIDE.md                # User documentation
│   └── API.md                       # API reference
│
├── 📁 tests/                        # Test suite
│   ├── test_parser.py               # Parser tests
│   ├── test_performance.py          # Performance tests
│   └── test_api.py                  # API tests
│
├── 📁 data/                         # Sample data
│   ├── resumes/                     # Resume files
│   └── job_descriptions/            # Job description files
│
├── 📁 output/                       # Analysis results
├── 📁 logs/                         # Application logs
│
├── 📄 cli.py                        # Command-line interface
├── 📄 requirements.txt               # Python dependencies
├── 📄 setup.py                      # Installation script
├── 📄 Makefile                      # Build automation
├── 📄 README.md                     # Project overview
├── 📄 QUICK_START.md                # Quick start guide
├── 📄 LICENSE                       # MIT License
└── 📄 .gitignore                    # Git ignore rules
```

## 📋 **Directory Descriptions**

### 🔧 **Core Application (`src/`)**
Contains the main application logic and AI components:
- **`main_pipeline.py`**: Orchestrates the entire resume screening process
- **`parser.py`**: Handles multi-format file parsing (PDF, DOCX, DOC, TXT)
- **`preprocess.py`**: Text cleaning and normalization
- **`scorer.py`**: ATS scoring and job matching algorithms
- **`skills_extractor.py`**: Technical and soft skill identification
- **`resume_analyzer.py`**: Comprehensive resume analysis engine
- **`performance_monitor.py`**: Real-time performance tracking
- **`utils.py`**: Shared utility functions

### 🌐 **API Layer (`api/`)**
FastAPI REST API for programmatic access:
- **`main.py`**: All API endpoints and request handling
- **Features**: File upload, batch processing, health monitoring
- **Documentation**: Auto-generated Swagger UI at `/docs`

### 🖥️ **Web Interface (`app/`)**
Streamlit web application for user interaction:
- **`main.py`**: Main web application with dashboard
- **`components/`**: Reusable UI components
- **Features**: File upload, real-time analysis, visualizations

### ⚙️ **Configuration (`config/`)**
Centralized configuration management:
- **`settings.py`**: Environment-based configuration
- **Features**: NLP, scoring, performance, API, database settings

### 🐳 **Docker (`docker/`)**
Containerization and deployment:
- **`Dockerfile`**: Production-ready container definition
- **`docker-compose.yml`**: Multi-service development environment
- **Services**: Web app, API, Redis, PostgreSQL

### 🚀 **Deployment (`deployment/`)**
Production deployment automation:
- **`deploy.sh`**: Automated deployment scripts
- **Features**: Cloud deployment, environment setup

### 📚 **Documentation (`docs/`)**
Comprehensive project documentation:
- **`api/`**: API documentation and examples
- **`deployment/`**: Deployment guides and instructions
- **`development/`**: Development guides and improvements
- **`USER_GUIDE.md`**: End-user documentation
- **`API.md`**: API reference documentation

### 🧪 **Testing (`tests/`)**
Comprehensive test suite:
- **`test_parser.py`**: File parsing and format tests
- **`test_performance.py`**: Performance monitoring tests
- **`test_api.py`**: API endpoint and integration tests
- **Coverage**: 15+ tests covering all major functionality

### 📊 **Data & Output (`data/`, `output/`, `logs/`)**
Data management and results:
- **`data/`**: Sample resumes and job descriptions
- **`output/`**: Analysis results and reports
- **`logs/`**: Application logs and performance metrics

## 🎯 **Key Benefits of This Structure**

### ✅ **Separation of Concerns**
- **API layer** separate from web interface
- **Configuration** centralized and environment-based
- **Documentation** organized by audience and purpose
- **Testing** comprehensive and well-structured

### ✅ **Scalability**
- **Modular design** allows easy feature additions
- **Docker support** enables containerized deployment
- **API-first approach** supports multiple frontends
- **Configuration-driven** for different environments

### ✅ **Maintainability**
- **Clear organization** makes code easy to find
- **Comprehensive documentation** for all components
- **Testing coverage** ensures code quality
- **Standard structure** follows best practices

### ✅ **Developer Experience**
- **Quick start** guides for new developers
- **Interactive documentation** for API usage
- **Docker setup** for consistent development environment
- **CLI tools** for command-line operations

## 🚀 **Usage Patterns**

### **Development**
```bash
# Local development
python cli.py --resume data/resumes/resume.pdf --job data/jobs/job.txt

# Web interface
streamlit run app/main.py

# API server
python api/main.py
```

### **Testing**
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/test_api.py -v
python -m pytest tests/test_performance.py -v
```

### **Deployment**
```bash
# Docker deployment
docker-compose up --build

# Production deployment
docker build -t apexhire:latest .
docker run -p 8000:8000 apexhire:latest
```

### **Documentation**
```bash
# API documentation
open http://localhost:8000/docs

# User guide
open docs/USER_GUIDE.md

# API reference
open docs/API.md
```

## 📈 **Project Evolution**

### **Phase 1: Core Application** ✅
- Resume parsing and analysis
- ATS scoring algorithms
- Web interface with Streamlit

### **Phase 2: API Layer** ✅
- FastAPI REST endpoints
- Performance monitoring
- Comprehensive testing

### **Phase 3: Production Ready** ✅
- Docker containerization
- Configuration management
- Deployment automation

### **Phase 4: Enterprise Features** 🔮
- Authentication and authorization
- Database integration
- Advanced analytics
- Cloud deployment

## 🏆 **Status: PRODUCTION READY**

This organized structure provides:
- **✅ Clear separation** of concerns
- **✅ Scalable architecture** for growth
- **✅ Comprehensive documentation** for all users
- **✅ Testing coverage** for quality assurance
- **✅ Docker support** for deployment
- **✅ API-first design** for flexibility

**Next Steps**: Deploy to production, add authentication, integrate with databases

---

**Structure Version**: 2.0.0
**Last Updated**: January 2024
**Status**: ✅ **Well-Organized & Production Ready**
