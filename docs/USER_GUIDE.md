# 🚀 ApexHire User Guide - Complete Usage Instructions

## �� Table of Contents
1. [Getting Started](#getting-started)
2. [Web Interface Usage](#web-interface-usage)
3. [Command Line Usage](#command-line-usage)
4. [File Requirements](#file-requirements)
5. [Understanding Results](#understanding-results)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Features](#advanced-features)

## 🎯 Getting Started

### Prerequisites
- Python 3.8 or higher
- Internet connection (for first-time setup)
- Resume files in PDF, DOCX, or TXT format
- Job description files in TXT format

### Installation
```bash
# Clone the repository
git clone https://github.com/ShashankBejjanki1241/ApexHire.git
cd ApexHire

# Run the automated setup
python setup.py

# Or use the deployment script
./scripts/deployment/deploy.sh
```

## 🌐 Web Interface Usage

### Starting the Web Interface
```bash
streamlit run app/main.py
```

### Step-by-Step Web Interface Guide

#### 1. 🏠 Home Page
- **Overview**: Learn about ApexHire's capabilities
- **Features**: View supported formats and capabilities
- **Statistics**: See system performance metrics

#### 2. 📄 Resume Analysis
**Step 1: Upload Resume**
- Click "Browse files" or drag and drop your resume
- Supported formats: PDF, DOCX, TXT
- Maximum file size: 10MB

**Step 2: Analyze**
- Click "🔍 Analyze Resume" button
- Wait for processing (usually 10-30 seconds)
- View results in the analysis section

**Step 3: Review Results**
- **Basic Information**: Text length, word count
- **Skills Found**: Technical and soft skills extracted
- **Processing Time**: How long the analysis took

#### 3. 💼 Job Matching
**Step 1: Enter Job Details**
- **Job Title**: Enter the position title (e.g., "Senior iOS Developer")
- **Job Description**: Paste the complete job description

**Step 2: Select Resume**
- Choose from previously uploaded resumes
- Or upload a new resume

**Step 3: Match Analysis**
- Click "🎯 Match Resume to Job"
- View detailed match results

**Step 4: Interpret Results**
- **Match Score**: Percentage match (0-100%)
- **Score Breakdown**: Keyword, semantic, skill, experience scores
- **Recommendations**: System suggestions based on score

#### 4. 📊 Results Page
- View all previous analysis results
- Compare different resumes and jobs
- Export results for further analysis

#### 5. ⚙️ Settings
- **Scoring Weights**: Adjust algorithm parameters
- **System Information**: View project paths and configurations
- **Save Settings**: Apply custom configurations

### Understanding Match Scores

| Score Range | Interpretation | Recommendation |
|-------------|----------------|----------------|
| 80-100% | 🎉 Excellent Match | Highly qualified candidate |
| 60-79% | 👍 Good Match | Consider for position |
| 40-59% | ⚠️ Moderate Match | Additional screening recommended |
| 0-39% | ❌ Low Match | Consider other candidates |

## 💻 Command Line Usage

### Basic Commands

#### Single Resume Analysis
```bash
# Analyze a single resume
python cli.py --resume data/resumes/my_resume.pdf

# Match resume to job description
python cli.py --resume data/resumes/my_resume.pdf --job data/jobs/ios_developer.txt
```

#### Batch Processing
```bash
# Process multiple resumes against multiple jobs
python cli.py --batch --resumes data/resumes/ --jobs data/jobs/ --output results.json
```

#### Web Interface Launch
```bash
# Launch web interface
python cli.py --web
```

### Advanced CLI Options
```bash
# Verbose output with detailed analysis
python cli.py --resume resume.pdf --job job.txt --verbose

# Custom output file
python cli.py --resume resume.pdf --job job.txt --output custom_results.json
```

## 📄 File Requirements

### Resume Files
**Supported Formats:**
- ✅ PDF (.pdf) - Most common format
- ✅ DOCX (.docx) - Microsoft Word documents
- ✅ TXT (.txt) - Plain text files

**File Requirements:**
- Maximum size: 10MB
- Text content: At least 100 characters
- Language: English (for best results)

**Best Practices:**
- Use clear, well-formatted resumes
- Include technical skills and experience
- Avoid heavily formatted PDFs with images
- Ensure text is readable and not scanned

### Job Description Files
**Format:** Plain text (.txt) files

**Content Requirements:**
- Clear job title and requirements
- Technical skills and qualifications
- Experience requirements
- Responsibilities and duties

**Example Job Description:**
```
Senior iOS Developer

Requirements:
- 5+ years iOS development experience
- Proficiency in Swift and Objective-C
- Experience with UIKit, Core Data, Core Animation
- Knowledge of RESTful APIs and third-party libraries
- Familiarity with Git and Agile methodologies
- Experience with Xcode and debugging tools

Responsibilities:
- Develop new iOS features and maintain existing apps
- Collaborate with cross-functional teams
- Write clean, modular, reusable code
- Perform code reviews and mentor junior developers
- Optimize app performance and troubleshoot issues
```

## 📊 Understanding Results

### Resume Analysis Results
```json
{
    "filename": "resume.pdf",
    "text_length": 12345,
    "word_count": 2345,
    "skills": {
        "technical_skills": ["python", "aws", "sql", "git"],
        "soft_skills": ["leadership", "communication", "agile"]
    },
    "processing_time": 2.34
}
```

### Job Match Results
```json
{
    "resume_filename": "resume.pdf",
    "overall_score": 0.75,
    "breakdown": {
        "keyword_score": 0.80,
        "semantic_score": 0.70,
        "skill_score": 0.75,
        "experience_score": 0.60
    },
    "skills_found": {
        "technical_skills": ["python", "aws"],
        "soft_skills": ["leadership"]
    }
}
```

### Score Breakdown Explanation
- **Keyword Score**: Exact word matches between resume and job
- **Semantic Score**: Meaning-based similarity using AI
- **Skill Score**: Technical and soft skill alignment
- **Experience Score**: Experience level matching

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. File Upload Issues
**Problem**: "Failed to upload file"
**Solution**: 
- Check file format (PDF, DOCX, TXT only)
- Ensure file size < 10MB
- Try converting to different format

#### 2. Analysis Fails
**Problem**: "Analysis failed" or "Error processing file"
**Solution**:
- Check file is not corrupted
- Ensure file contains readable text
- Try with a different resume file

#### 3. Low Match Scores
**Problem**: Consistently low match scores
**Solution**:
- Improve job description clarity
- Add more specific requirements
- Check resume format and content

#### 4. Web Interface Not Loading
**Problem**: Streamlit app doesn't start
**Solution**:
```bash
# Check dependencies
pip install -r requirements.txt

# Try different port
streamlit run app/main.py --server.port 8501

# Check Python version
python --version
```

#### 5. Memory Issues
**Problem**: "Out of memory" errors
**Solution**:
- Close other applications
- Use smaller files
- Process files one at a time

### Performance Tips
- **Smaller files**: Process faster and use less memory
- **Batch processing**: More efficient for multiple files
- **Clear formatting**: Better text extraction results
- **Regular updates**: Keep dependencies updated

## 🚀 Advanced Features

### Custom Scoring Weights
Adjust the algorithm parameters in Settings:
- **Keyword Similarity**: 0.4 (default)
- **Semantic Similarity**: 0.3 (default)
- **Skill Match**: 0.2 (default)
- **Experience Score**: 0.1 (default)

### Batch Processing
For processing multiple files:
1. Place all resumes in `data/resumes/`
2. Place all job descriptions in `data/jobs/`
3. Use batch processing for efficiency

### Export Results
- Results are automatically saved to `output/` directory
- JSON format for programmatic access
- CSV format for spreadsheet analysis

### API Integration
For developers, see `docs/API.md` for programmatic access.

## 📞 Support

### Getting Help
- **Documentation**: Check this guide and API docs
- **GitHub Issues**: Report bugs and feature requests
- **Examples**: See sample files in `data/` directory

### Contact Information
- **Author**: Shashank B
- **GitHub**: [@ShashankBejjanki1241](https://github.com/ShashankBejjanki1241)
- **Project**: [ApexHire](https://github.com/ShashankBejjanki1241/ApexHire)

---

⭐ **Star this project** if you find it helpful!
