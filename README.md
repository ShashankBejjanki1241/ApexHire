# 🚀 ApexHire - AI Resume Screener

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red.svg)](https://streamlit.io/)
[![spaCy](https://img.shields.io/badge/spaCy-NLP-green.svg)](https://spacy.io/)

An intelligent, end-to-end system that automatically reads, analyzes, scores, and ranks resumes based on job descriptions. Built with Python and Natural Language Processing (NLP), this system mimics what a human recruiter does—but faster and more consistently.

## ⚡ Quick Start (5 Minutes)

### 1. Setup
```bash
git clone https://github.com/ShashankBejjanki1241/ApexHire.git
cd ApexHire
python setup.py
```

### 2. Launch Web Interface
```bash
streamlit run app/main.py
```

### 3. Use the System
- **Upload Resume**: Go to "📄 Resume Analysis" and upload your resume
- **Add Job**: Go to "💼 Job Matching" and enter job details
- **Get Results**: View match scores and recommendations

## 🎯 Perfect For

| Use Case | Description |
|----------|-------------|
| **Job Seekers** | Test your resume against job descriptions |
| **Recruiters** | Screen multiple candidates efficiently |
| **HR Teams** | Standardize resume evaluation |
| **Career Coaches** | Help clients improve resumes |

## 🛠️ Features

- **📄 Resume Parsing**: Supports PDF, DOCX, and TXT formats
- **🧹 Text Preprocessing**: Cleans and tokenizes text data
- **🧠 Skill Extraction**: Extracts technical and soft skills
- **📊 Relevance Scoring**: Matches resumes against job descriptions
- **🌐 Web Interface**: Streamlit-based user interface
- **📈 Ranking System**: Ranks candidates by relevance score
- **🔍 Semantic Analysis**: Advanced NLP for better matching
- **📋 Detailed Reports**: Comprehensive analysis output

## 🛠️ Tech Stack

- **Python 3.8+**
- **spaCy** - Natural Language Processing
- **pdfplumber** - PDF text extraction
- **python-docx** - DOCX file handling
- **pandas & numpy** - Data processing
- **scikit-learn** - Machine learning utilities
- **Streamlit** - Web application framework
- **NLTK** - Natural Language Toolkit

## 🚀 Usage Options

### 🌐 Web Interface (Recommended)
```bash
streamlit run app/main.py
```
**Features:**
- Easy-to-use dashboard
- Real-time analysis
- Interactive visualizations
- Step-by-step guidance

### 💻 Command Line
```bash
# Single file analysis
python cli.py --resume resume.pdf --job job.txt

# Batch processing
python cli.py --batch --resumes data/resumes/ --jobs data/jobs/

# Launch web interface
python cli.py --web
```

### 🔧 Programmatic API
```python
from src.main_pipeline import ResumeScreener

screener = ResumeScreener()
result = screener.analyze_resume("resume.pdf")
match = screener.match_resume_to_job("resume.pdf", job_description)
```

## 📁 Project Structure

```
ApexHire/
├── 📁 src/                     # Core AI modules
│   ├── main_pipeline.py        # Main orchestration
│   ├── parser.py               # Resume parsing
│   ├── preprocess.py           # Text preprocessing
│   ├── scorer.py               # Scoring algorithms
│   ├── skills_extractor.py     # Skill extraction
│   ├── utils.py                # Utility functions
│   └── config/settings.py      # Configuration
├── 📁 app/                     # Web interface
│   ├── main.py                 # Streamlit app
│   └── components/analytics.py # Analytics dashboard
├── 📁 docs/                    # Documentation
│   ├── USER_GUIDE.md          # Complete user guide
│   └── API.md                 # API documentation
├── 📁 scripts/                 # Deployment scripts
├── 📁 tests/                   # Test suite
├── 📄 requirements.txt         # Dependencies
├── 📄 setup.py                 # Installation script
├── 📄 cli.py                   # Command-line interface
└── 📄 README.md                # This file
```

## 📊 Example Results

```
🎯 RESUME ANALYSIS RESULTS
==========================================
📄 Resume: example_resume.pdf
📊 Text Length: 12,176 characters
🔧 Technical Skills: python, aws, sql, git, react
🤝 Soft Skills: agile, scrum, leadership

📊 JOB MATCH SCORES:
----------------------------------------
iOS Developer: 0.453 (45.3%)
Full Stack Developer: 0.447 (44.7%)
Python Developer: 0.470 (47.0%)
```

## 📋 File Requirements

### Resume Files
- **Formats**: PDF, DOCX, TXT
- **Size**: Maximum 10MB
- **Content**: Readable text (not scanned images)
- **Language**: English (for best results)

### Job Descriptions
- **Format**: Plain text (.txt)
- **Content**: Clear requirements and responsibilities
- **Length**: Detailed descriptions work better

## 🔧 Configuration

The system can be customized by modifying:
- **Scoring weights** in `src/config/settings.py`
- **Skill lists** in `src/skills_extractor.py`
- **Text preprocessing** in `src/preprocess.py`

## 📚 Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get started in 5 minutes
- **[Complete User Guide](docs/USER_GUIDE.md)** - Detailed instructions
- **[API Documentation](docs/API.md)** - For developers
- **[Troubleshooting](docs/USER_GUIDE.md#troubleshooting)** - Common issues

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Shashank B**
- GitHub: [@ShashankBejjanki1241](https://github.com/ShashankBejjanki1241)
- Project: [ApexHire](https://github.com/ShashankBejjanki1241/ApexHire)

## 🙏 Acknowledgments

- **spaCy** for excellent NLP capabilities
- **pdfplumber** for reliable PDF parsing
- **python-docx** for DOCX file handling
- **pandas** and **numpy** for data processing
- **Streamlit** for web interface framework

---

⭐ **Star this repository** if you find it helpful!

🔄 **Fork and contribute** to make it even better!

📧 **Contact the author** for collaboration opportunities!
