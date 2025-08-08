# 🚀 AI Resume Screener - ApexHire

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red.svg)](https://streamlit.io/)
[![spaCy](https://img.shields.io/badge/spaCy-NLP-green.svg)](https://spacy.io/)

An intelligent, end-to-end system that automatically reads, analyzes, scores, and ranks resumes based on job descriptions. Built with Python and Natural Language Processing (NLP), this system mimics what a human recruiter does—but faster and more consistently.

## 🎯 Features

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

## 🚀 Quick Start

### Prerequisites
```bash
# Clone the repository
git clone https://github.com/ShashankBejjanki1241/ApexHire.git
cd ApexHire

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model (if needed)
python -m spacy download en_core_web_sm
```

### Usage
```bash
# Run the main pipeline
python src/main_pipeline.py

# Or run the web interface
streamlit run app/main.py
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
│   └── utils.py                # Utility functions
├── 📁 app/                     # Web interface
│   └── main.py                 # Streamlit app
├── 📁 data/                    # Data directories
│   ├── job_descriptions/       # Job description files
│   └── resumes/                # Resume files
├── 📄 requirements.txt         # Python dependencies
├── 📄 LICENSE                  # MIT License
└── 📄 README.md                # This file
```

## 📊 Example Output

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

## 🔧 Configuration

The system can be customized by modifying:
- **Scoring weights** in `src/scorer.py`
- **Skill lists** in `src/skills_extractor.py`
- **Text preprocessing** in `src/preprocess.py`

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

---

⭐ **Star this repository** if you find it helpful!
