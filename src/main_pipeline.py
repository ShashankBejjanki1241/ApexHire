"""
Main Pipeline Module
Orchestrates the complete AI Resume Screener workflow
"""

import os
import logging
from typing import List, Dict, Optional
from parser import ResumeParser
from preprocess import TextPreprocessor
from skills_extractor import SkillsExtractor
from scorer import ResumeScorer
from utils import (
    setup_logging, create_directory_structure, save_results_to_json,
    create_summary_report, save_summary_report, print_summary_report,
    print_dependency_status
)

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)


class ResumeScreenerPipeline:
    """Main pipeline for AI Resume Screener"""
    
    def __init__(self, use_semantic_similarity: bool = True):
        """Initialize the pipeline"""
        self.parser = ResumeParser()
        self.preprocessor = TextPreprocessor()
        self.skills_extractor = SkillsExtractor()
        self.scorer = ResumeScorer(use_semantic_similarity=use_semantic_similarity)
        
        # Create necessary directories
        create_directory_structure()
        
        logger.info("Resume Screener Pipeline initialized")
    
    def process_multiple_resumes(self, resume_directory: str) -> List[Dict]:
        """Process multiple resumes from a directory"""
        logger.info(f"Processing resumes from directory: {resume_directory}")
        
        # Parse all resumes
        parsed_resumes = self.parser.parse_multiple_resumes(resume_directory)
        
        if not parsed_resumes:
            logger.warning(f"No resumes found in directory: {resume_directory}")
            return []
        
        processed_resumes = []
        
        for parsed_resume in parsed_resumes:
            # Preprocess text
            preprocessed = self.preprocessor.preprocess_text(parsed_resume['text'])
            
            # Extract skills and information
            skills_info = self.skills_extractor.extract_all_skills_and_info(parsed_resume['text'])
            
            # Combine all data
            processed_resume = {
                'filename': parsed_resume['filename'],
                'file_path': parsed_resume['file_path'],
                'text': parsed_resume['text'],
                'preprocessed': preprocessed,
                'skills': skills_info
            }
            
            processed_resumes.append(processed_resume)
        
        logger.info(f"Successfully processed {len(processed_resumes)} resumes")
        return processed_resumes
    
    def screen_resumes(self, resume_directory: str, job_description: str, 
                      output_file: str = 'output/results.csv') -> List[Dict]:
        """Complete resume screening workflow"""
        logger.info("Starting resume screening workflow")
        
        # Step 1: Process all resumes
        processed_resumes = self.process_multiple_resumes(resume_directory)
        
        if not processed_resumes:
            logger.error("No resumes processed. Cannot continue screening.")
            return []
        
        # Step 2: Rank resumes against job description
        ranked_resumes = self.scorer.rank_resumes(processed_resumes, job_description)
        
        if not ranked_resumes:
            logger.error("No resumes ranked. Check job description and resume data.")
            return []
        
        # Step 3: Create and save summary report
        summary_report = create_summary_report(ranked_resumes, job_description)
        save_summary_report(summary_report)
        
        # Step 4: Print summary
        print_summary_report(summary_report)
        
        logger.info("Resume screening workflow completed successfully")
        return ranked_resumes


def main():
    """Main function to run the resume screener"""
    print("🚀 AI Resume Screener - Main Pipeline")
    print("="*50)
    
    # Check dependencies
    print_dependency_status()
    
    # Initialize pipeline
    pipeline = ResumeScreenerPipeline()
    
    # Check if we have resumes to process
    resume_dir = 'data/resumes'
    if not os.path.exists(resume_dir) or not os.listdir(resume_dir):
        print(f"\n📁 No resumes found in {resume_dir}")
        print("Please add resume files (PDF/DOCX) to the data/resumes/ directory")
        print("Then run the pipeline again.")
        return
    
    # Create sample job description
    sample_job_description = """
    Senior Software Engineer
    
    We are looking for a Senior Software Engineer with the following requirements:
    
    Technical Skills:
    - Python programming (3+ years)
    - JavaScript/React development
    - AWS cloud services
    - Docker containerization
    - Git version control
    - SQL databases (MySQL, PostgreSQL)
    
    Experience:
    - 5+ years of software development experience
    - Experience leading small teams
    - Experience with agile methodologies
    
    Education:
    - Bachelor's degree in Computer Science or related field
    
    Responsibilities:
    - Develop and maintain web applications
    - Lead technical projects
    - Mentor junior developers
    - Collaborate with cross-functional teams
    """
    
    print(f"\n📄 Using sample job description")
    print(f"📁 Processing resumes from: {resume_dir}")
    
    # Run the screening
    results = pipeline.screen_resumes(
        resume_directory=resume_dir,
        job_description=sample_job_description
    )
    
    if results:
        print(f"\n✅ Screening completed! Processed {len(results)} resumes.")
        print("📊 Results saved to output/summary_report.json")
    else:
        print("\n❌ Screening failed. Check the logs for details.")


if __name__ == "__main__":
    main()
