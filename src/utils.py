"""
Utility Functions Module
Helper functions for the AI Resume Screener
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any

# Centralized logging setup
logger = logging.getLogger(__name__)


def setup_logging(log_file: str = 'logs/resume_screener.log', force: bool = False):
    """Setup centralized logging configuration
    
    Args:
        log_file: Path to log file
        force: Force reconfiguration even if already configured
    """
    # Check if logging is already configured
    if not force and logging.getLogger().handlers:
        logger = logging.getLogger(__name__)
        logger.debug("Logging already configured, returning existing logger")
        return logger
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ],
        force=force  # Force reconfiguration if needed
    )
    
    # Configure specific loggers
    loggers_to_configure = [
        'src.parser',
        'src.preprocess', 
        'src.scorer',
        'src.skills_extractor',
        'src.resume_analyzer',
        'src.main_pipeline',
        'api.main',
        'utils'
    ]
    
    for logger_name in loggers_to_configure:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        # Allow propagation to root logger for proper handling
        logger.propagate = True
    
    logger = logging.getLogger(__name__)
    logger.info(f"Centralized logging configured. Log file: {log_file}")
    
    return logger


def create_directory_structure():
    """Create necessary directories for the project"""
    directories = [
        'data/resumes',
        'data/job_descriptions',
        'output',
        'logs',
        'temp'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created directory: {directory}")


def print_dependency_status():
    """Print the status of all dependencies"""
    dependencies = {
        'spacy': False,
        'sentence_transformers': False,
        'sklearn': False,
        'pandas': False,
        'numpy': False,
        'pdfplumber': False,
        'python-docx': False
    }
    
    try:
        import pandas
        dependencies['pandas'] = True
    except ImportError:
        pass
    
    try:
        import numpy
        dependencies['numpy'] = True
    except ImportError:
        pass
    
    try:
        import spacy
        dependencies['spacy'] = True
    except ImportError:
        pass
    
    try:
        import pdfplumber
        dependencies['pdfplumber'] = True
    except ImportError:
        pass
    
    try:
        import sklearn
        dependencies['sklearn'] = True
    except ImportError:
        pass
    
    try:
        import sentence_transformers
        dependencies['sentence_transformers'] = True
    except ImportError:
        pass
    
    try:
        import docx
        dependencies['python-docx'] = True
    except ImportError:
        pass
    
    print("\n" + "="*40)
    print("DEPENDENCY STATUS")
    print("="*40)
    
    all_good = True
    for dep, status in dependencies.items():
        status_symbol = "✅" if status else "❌"
        print(f"   {status_symbol} {dep}")
        if not status:
            all_good = False
    
    if all_good:
        print("\n🎉 All dependencies are available!")
    else:
        print("\n⚠️  Some dependencies are missing. Please install them:")
        print("   pip install -r requirements.txt")
    
    print("="*40)


def create_summary_report(ranked_resumes, job_description: str):
    """Create a summary report of the screening results"""
    if not ranked_resumes:
        return {}
    
    # Calculate statistics
    total_resumes = len(ranked_resumes)
    avg_score = sum(r['score'] for r in ranked_resumes) / total_resumes
    max_score = max(r['score'] for r in ranked_resumes)
    min_score = min(r['score'] for r in ranked_resumes)
    
    # Top candidates
    top_candidates = ranked_resumes[:min(5, len(ranked_resumes))]
    
    report = {
        'summary': {
            'total_resumes': total_resumes,
            'average_score': round(avg_score, 3),
            'highest_score': round(max_score, 3),
            'lowest_score': round(min_score, 3),
            'job_description_length': len(job_description)
        },
        'top_candidates': [
            {
                'rank': i + 1,
                'filename': candidate['filename'],
                'score': round(candidate['score'], 3),
                'matched_skills': len(candidate['breakdown']['skill_details'].get('matched_skill_list', []))
            }
            for i, candidate in enumerate(top_candidates)
        ],
        'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S")
    }
    
    return report


def save_summary_report(report, output_file: str = 'output/summary_report.json'):
    """Save summary report to file"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Summary report saved to {output_file}")
        
    except Exception as e:
        logger.error(f"Error saving summary report: {e}")


def print_summary_report(report):
    """Print summary report to console"""
    if not report:
        print("No report data available")
        return
    
    print("\n" + "="*50)
    print("AI RESUME SCREENER - SUMMARY REPORT")
    print("="*50)
    
    summary = report.get('summary', {})
    print(f"\n📊 SCREENING STATISTICS:")
    print(f"   Total Resumes Processed: {summary.get('total_resumes', 0)}")
    print(f"   Average Score: {summary.get('average_score', 0):.3f}")
    print(f"   Highest Score: {summary.get('highest_score', 0):.3f}")
    print(f"   Lowest Score: {summary.get('lowest_score', 0):.3f}")
    
    print(f"\n🏆 TOP CANDIDATES:")
    top_candidates = report.get('top_candidates', [])
    for candidate in top_candidates:
        print(f"   #{candidate['rank']}: {candidate['filename']} (Score: {candidate['score']:.3f})")
    
    print(f"\n⏰ Generated: {report.get('timestamp', 'Unknown')}")
    print("="*50)


def save_results_to_json(results: Dict[str, Any], output_file: str = 'output/results.json'):
    """Save analysis results to JSON file"""
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving results: {e}")
        return False


def load_job_descriptions(jobs_dir: str = 'data/job_descriptions') -> Dict[str, str]:
    """Load job descriptions from directory"""
    job_descriptions = {}
    
    try:
        if not os.path.exists(jobs_dir):
            logger.warning(f"Job descriptions directory not found: {jobs_dir}")
            return job_descriptions
        
        for filename in os.listdir(jobs_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(jobs_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        job_name = filename.replace('.txt', '')
                        job_descriptions[job_name] = content
                        logger.info(f"Loaded job description: {filename}")
                except Exception as e:
                    logger.error(f"Error loading {filename}: {e}")
        
        logger.info(f"Loaded {len(job_descriptions)} job descriptions")
        return job_descriptions
        
    except Exception as e:
        logger.error(f"Error loading job descriptions: {e}")
        return job_descriptions


if __name__ == "__main__":
    print("Utility Functions Module")
