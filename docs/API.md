# ApexHire API Documentation

## Overview

ApexHire provides a comprehensive API for AI-powered resume screening and job matching. This document describes the main classes and methods available for integration.

## Core Classes

### ResumeScreener

The main class for resume screening operations.

```python
from src.main_pipeline import ResumeScreener

# Initialize the screener
screener = ResumeScreener()
```

#### Methods

##### `analyze_resume(resume_path: str) -> Optional[Dict[str, Any]]`

Analyzes a single resume and returns detailed results.

**Parameters:**
- `resume_path` (str): Path to the resume file

**Returns:**
- Dictionary containing analysis results or None if failed

**Example:**
```python
result = screener.analyze_resume("path/to/resume.pdf")
if result:
    print(f"Skills found: {result['skills']}")
    print(f"Text length: {result['text_length']}")
```

##### `match_resume_to_job(resume_path: str, job_description: str) -> Optional[Dict[str, Any]]`

Matches a resume against a specific job description.

**Parameters:**
- `resume_path` (str): Path to the resume file
- `job_description` (str): Job description text

**Returns:**
- Dictionary containing match results or None if failed

**Example:**
```python
job_desc = "We are looking for a Python developer..."
result = screener.match_resume_to_job("resume.pdf", job_desc)
if result:
    print(f"Match score: {result['overall_score']:.1%}")
```

##### `run_batch_analysis(resumes_dir: str, jobs_dir: str, output_file: str = None) -> Dict[str, Any]`

Runs batch analysis on multiple resumes and job descriptions.

**Parameters:**
- `resumes_dir` (str): Directory containing resume files
- `jobs_dir` (str): Directory containing job description files
- `output_file` (str, optional): Output file path

**Returns:**
- Dictionary containing batch analysis results

**Example:**
```python
results = screener.run_batch_analysis(
    "data/resumes/",
    "data/jobs/",
    "output/results.json"
)
```

##### `get_system_status() -> Dict[str, Any]`

Gets system status and health information.

**Returns:**
- Dictionary containing system status

**Example:**
```python
status = screener.get_system_status()
print(f"Parser available: {status['components']['parser']}")
```

## Configuration

### Settings

The system uses a centralized configuration file at `src/config/settings.py`.

**Key Settings:**
- `SCORING_WEIGHTS`: Weights for different scoring components
- `SUPPORTED_FORMATS`: Supported file formats
- `TECHNICAL_SKILLS`: List of technical skills to extract
- `SOFT_SKILLS`: List of soft skills to extract

**Example:**
```python
import config.settings as settings

# Modify scoring weights
settings.SCORING_WEIGHTS['keyword_similarity'] = 0.5
settings.SCORING_WEIGHTS['semantic_similarity'] = 0.3
```

## Error Handling

All methods include comprehensive error handling and logging.

**Example:**
```python
try:
    result = screener.analyze_resume("resume.pdf")
    if result:
        print("Analysis successful")
    else:
        print("Analysis failed")
except Exception as e:
    print(f"Error: {str(e)}")
```

## Output Formats

### Resume Analysis Output

```json
{
    "filename": "resume.pdf",
    "text_length": 12345,
    "word_count": 2345,
    "skills": {
        "technical_skills": ["python", "aws", "sql"],
        "soft_skills": ["leadership", "communication"]
    },
    "processing_time": 2.34,
    "raw_text": "First 1000 characters...",
    "processed_text": "Processed text preview..."
}
```

### Job Match Output

```json
{
    "resume_filename": "resume.pdf",
    "overall_score": 0.75,
    "breakdown": {
        "keyword_score": 0.8,
        "semantic_score": 0.7,
        "skill_score": 0.75,
        "experience_score": 0.6
    },
    "skills_found": {
        "technical_skills": ["python", "aws"],
        "soft_skills": ["leadership"]
    },
    "processing_time": 3.45
}
```

### Batch Analysis Output

```json
{
    "summary": {
        "total_resumes": 5,
        "total_jobs": 3,
        "total_matches": 15,
        "average_score": 0.68,
        "processing_time": 12.34
    },
    "results": [
        {
            "resume_filename": "resume1.pdf",
            "resume_analysis": {...},
            "job_matches": [...]
        }
    ],
    "timestamp": "2024-08-07 21:30:00"
}
```

## Performance Considerations

- **File Size**: Maximum file size is 10MB
- **Text Length**: Maximum text length is 50,000 characters
- **Batch Size**: Process files in batches of 10 for optimal performance
- **Memory**: Large files may require additional memory

## Logging

The system uses Python's logging module for comprehensive logging.

**Log Levels:**
- INFO: General information
- WARNING: Non-critical issues
- ERROR: Critical errors
- DEBUG: Detailed debugging information

## Best Practices

1. **Error Handling**: Always check return values for None
2. **File Validation**: Validate file formats before processing
3. **Resource Management**: Close files and clean up resources
4. **Configuration**: Use settings file for customization
5. **Logging**: Monitor logs for system health

## Examples

### Complete Workflow

```python
from src.main_pipeline import ResumeScreener
import config.settings as settings

# Initialize
screener = ResumeScreener()

# Check system status
status = screener.get_system_status()
print(f"System ready: {all(status['components'].values())}")

# Analyze single resume
result = screener.analyze_resume("resume.pdf")
if result:
    print(f"Found {len(result['skills']['technical_skills'])} technical skills")

# Match against job
job_desc = "Python developer with AWS experience..."
match = screener.match_resume_to_job("resume.pdf", job_desc)
if match:
    print(f"Match score: {match['overall_score']:.1%}")

# Batch processing
results = screener.run_batch_analysis(
    "data/resumes/",
    "data/jobs/",
    "output/batch_results.json"
)
print(f"Processed {results['summary']['total_matches']} matches")
```
