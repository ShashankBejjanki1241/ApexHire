"""
Configuration settings for ApexHire AI Resume Screener
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RESUMES_DIR = DATA_DIR / "resumes"
JOBS_DIR = DATA_DIR / "job_descriptions"
OUTPUT_DIR = PROJECT_ROOT / "output"
LOGS_DIR = PROJECT_ROOT / "logs"

# File extensions
SUPPORTED_FORMATS = ['.pdf', '.docx', '.doc', '.txt']

# Scoring weights
SCORING_WEIGHTS = {
    'keyword_similarity': 0.4,
    'semantic_similarity': 0.3,
    'skill_match': 0.2,
    'experience_score': 0.1
}

# Skill categories
TECHNICAL_SKILLS = [
    'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mongodb',
    'aws', 'azure', 'docker', 'kubernetes', 'git', 'jenkins', 'agile',
    'swift', 'kotlin', 'flutter', 'dart', 'html', 'css', 'bootstrap',
    'django', 'flask', 'fastapi', 'spring', 'express', 'angular', 'vue',
    'typescript', 'php', 'c++', 'c#', '.net', 'ruby', 'rails', 'go',
    'rust', 'scala', 'r', 'matlab', 'tensorflow', 'pytorch', 'scikit-learn',
    'pandas', 'numpy', 'spark', 'hadoop', 'kafka', 'redis', 'elasticsearch'
]

SOFT_SKILLS = [
    'leadership', 'communication', 'teamwork', 'problem solving',
    'critical thinking', 'creativity', 'adaptability', 'time management',
    'project management', 'agile', 'scrum', 'kanban', 'collaboration',
    'mentoring', 'presentation', 'negotiation', 'customer service'
]

# Logging configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Output settings
OUTPUT_FORMATS = ['json', 'csv', 'txt']
DEFAULT_OUTPUT_FORMAT = 'json'

# Web interface settings
STREAMLIT_CONFIG = {
    'page_title': 'ApexHire - AI Resume Screener',
    'page_icon': '📄',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Performance settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_TEXT_LENGTH = 50000  # characters
BATCH_SIZE = 10  # for processing multiple files

# Create directories if they don't exist
def ensure_directories():
    """Create necessary directories"""
    directories = [RESUMES_DIR, JOBS_DIR, OUTPUT_DIR, LOGS_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Initialize directories
ensure_directories()
