"""
Configuration settings for ApexHire AI Resume Screener
"""

import os
from pathlib import Path
from typing import Dict, Any

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# File paths
RESUMES_DIR = DATA_DIR / "resumes"
JOBS_DIR = DATA_DIR / "job_descriptions"
DEFAULT_OUTPUT_FILE = OUTPUT_DIR / "results.json"

# Supported file formats
SUPPORTED_FORMATS = ['.pdf', '.docx', '.doc', '.txt']

# NLP Configuration
NLP_CONFIG = {
    'spacy_model': 'en_core_web_sm',
    'min_skill_confidence': 0.7,
    'max_text_length': 50000,
    'min_text_length': 100
}

# Scoring Configuration
SCORING_CONFIG = {
    'experience_weight': 0.3,
    'skills_weight': 0.4,
    'education_weight': 0.2,
    'other_weight': 0.1,
    'min_experience_years': 0,
    'max_experience_years': 50,
    'skill_match_threshold': 0.6
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'max_processing_time': 30,  # seconds
    'batch_size': 10,
    'memory_limit_mb': 512,
    'enable_caching': True,
    'cache_ttl': 3600  # 1 hour
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': LOGS_DIR / 'apexhire.log',
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# Web Interface Configuration
WEB_CONFIG = {
    'page_title': 'ApexHire - AI Resume Screener',
    'page_icon': '📄',
    'layout': 'wide',
    'max_file_size_mb': 10,
    'allowed_file_types': ['pdf', 'docx', 'doc', 'txt']
}

# API Configuration (for future use)
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 8000,
    'debug': False,
    'reload': True,
    'workers': 1
}

# Database Configuration (for future use)
DATABASE_CONFIG = {
    'url': os.getenv('DATABASE_URL', 'sqlite:///apexhire.db'),
    'echo': False,
    'pool_size': 10,
    'max_overflow': 20
}

# AWS Configuration (for future cloud deployment)
AWS_CONFIG = {
    'region': os.getenv('AWS_REGION', 'us-east-1'),
    's3_bucket': os.getenv('S3_BUCKET', 'apexhire-resumes'),
    'access_key': os.getenv('AWS_ACCESS_KEY_ID'),
    'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY')
}

# Security Configuration
SECURITY_CONFIG = {
    'secret_key': os.getenv('SECRET_KEY', 'your-secret-key-here'),
    'algorithm': 'HS256',
    'access_token_expire_minutes': 30,
    'max_login_attempts': 5,
    'lockout_duration_minutes': 15
}

def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        DATA_DIR,
        RESUMES_DIR,
        JOBS_DIR,
        OUTPUT_DIR,
        LOGS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def get_config() -> Dict[str, Any]:
    """Get complete configuration dictionary"""
    return {
        'base_dir': str(BASE_DIR),
        'data_dir': str(DATA_DIR),
        'output_dir': str(OUTPUT_DIR),
        'logs_dir': str(LOGS_DIR),
        'supported_formats': SUPPORTED_FORMATS,
        'nlp_config': NLP_CONFIG,
        'scoring_config': SCORING_CONFIG,
        'performance_config': PERFORMANCE_CONFIG,
        'logging_config': LOGGING_CONFIG,
        'web_config': WEB_CONFIG,
        'api_config': API_CONFIG,
        'database_config': DATABASE_CONFIG,
        'aws_config': AWS_CONFIG,
        'security_config': SECURITY_CONFIG
    }

def validate_config() -> bool:
    """Validate configuration settings with comprehensive checks"""
    try:
        # Check if required directories can be created
        ensure_directories()
        
        # Validate scoring weights sum to 1
        weights = SCORING_CONFIG['experience_weight'] + \
                 SCORING_CONFIG['skills_weight'] + \
                 SCORING_CONFIG['education_weight'] + \
                 SCORING_CONFIG['other_weight']
        
        if abs(weights - 1.0) > 0.01:
            raise ValueError(f"Scoring weights must sum to 1.0, got {weights:.3f}")
        
        # Validate individual scoring weights are between 0 and 1
        weight_fields = ['experience_weight', 'skills_weight', 'education_weight', 'other_weight']
        for key in weight_fields:
            weight = SCORING_CONFIG[key]
            if not isinstance(weight, (int, float)) or weight < 0 or weight > 1:
                raise ValueError(f"Scoring weight '{key}' must be between 0 and 1, got {weight}")
        
        # Validate other scoring configuration values
        if SCORING_CONFIG['min_experience_years'] < 0:
            raise ValueError("min_experience_years must be non-negative")
        
        if SCORING_CONFIG['max_experience_years'] <= 0:
            raise ValueError("max_experience_years must be positive")
        
        if SCORING_CONFIG['min_experience_years'] >= SCORING_CONFIG['max_experience_years']:
            raise ValueError("min_experience_years must be less than max_experience_years")
        
        if not isinstance(SCORING_CONFIG['skill_match_threshold'], (int, float)) or \
           SCORING_CONFIG['skill_match_threshold'] < 0 or SCORING_CONFIG['skill_match_threshold'] > 1:
            raise ValueError("skill_match_threshold must be between 0 and 1")
        
        # Validate performance settings
        if PERFORMANCE_CONFIG['max_processing_time'] <= 0:
            raise ValueError("Max processing time must be positive")
        
        if PERFORMANCE_CONFIG['memory_limit_mb'] <= 0:
            raise ValueError("Memory limit must be positive")
        
        if PERFORMANCE_CONFIG['batch_size'] <= 0:
            raise ValueError("Batch size must be positive")
        
        if PERFORMANCE_CONFIG['cache_ttl'] <= 0:
            raise ValueError("Cache TTL must be positive")
        
        # Validate NLP configuration
        if not isinstance(NLP_CONFIG['min_skill_confidence'], (int, float)) or \
           NLP_CONFIG['min_skill_confidence'] < 0 or NLP_CONFIG['min_skill_confidence'] > 1:
            raise ValueError("min_skill_confidence must be between 0 and 1")
        
        if NLP_CONFIG['max_text_length'] <= 0:
            raise ValueError("max_text_length must be positive")
        
        if NLP_CONFIG['min_text_length'] <= 0:
            raise ValueError("min_text_length must be positive")
        
        if NLP_CONFIG['min_text_length'] >= NLP_CONFIG['max_text_length']:
            raise ValueError("min_text_length must be less than max_text_length")
        
        # Validate file format configurations
        if not SUPPORTED_FORMATS:
            raise ValueError("SUPPORTED_FORMATS cannot be empty")
        
        # Validate logging configuration
        if LOGGING_CONFIG['max_file_size'] <= 0:
            raise ValueError("Log max file size must be positive")
        
        if LOGGING_CONFIG['backup_count'] < 0:
            raise ValueError("Log backup count must be non-negative")
        
        # Validate API configuration
        if API_CONFIG['port'] <= 0 or API_CONFIG['port'] > 65535:
            raise ValueError("API port must be between 1 and 65535")
        
        if API_CONFIG['workers'] <= 0:
            raise ValueError("API workers must be positive")
        
        # Validate security configuration
        if SECURITY_CONFIG['access_token_expire_minutes'] <= 0:
            raise ValueError("Access token expire minutes must be positive")
        
        if SECURITY_CONFIG['max_login_attempts'] <= 0:
            raise ValueError("Max login attempts must be positive")
        
        if SECURITY_CONFIG['lockout_duration_minutes'] <= 0:
            raise ValueError("Lockout duration must be positive")
        
        print("✅ Configuration validation passed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

# Initialize directories on import
ensure_directories()
