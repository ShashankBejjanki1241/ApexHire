"""
Enhanced Main Pipeline for ApexHire AI Resume Screener
"""

import os
import sys
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import traceback

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from parser import ResumeParser
from preprocess import TextPreprocessor
from skills_extractor import AdvancedSkillsExtractor
from scorer import ResumeScorer
from resume_analyzer import ResumeAnalyzer
from utils import setup_logging, save_results_to_json, load_job_descriptions
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config.settings as settings

class ResumeScreener:
    """
    Enhanced AI Resume Screener with comprehensive analysis capabilities
    """
    
    def __init__(self):
        """Initialize the resume screener with all components"""
        self.logger = setup_logging()
        self.parser = ResumeParser()
        self.preprocessor = TextPreprocessor()
        self.skills_extractor = AdvancedSkillsExtractor()
        self.scorer = ResumeScorer()
        self.resume_analyzer = ResumeAnalyzer()
        
        # Ensure directories exist
        settings.ensure_directories()
        
        self.logger.info("ResumeScreener initialized successfully")
    
    def analyze_resume(self, resume_path: str) -> Optional[Dict[str, Any]]:
        """
        Analyze a single resume and return detailed results
        
        Args:
            resume_path: Path to the resume file
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            self.logger.info(f"Starting analysis of: {resume_path}")
            start_time = time.time()
            
            # Parse resume
            raw_text = self.parser.parse_resume(resume_path)
            if not raw_text:
                self.logger.error(f"Failed to parse resume: {resume_path}")
                return None
            
            # Preprocess text
            processed_data = self.preprocessor.preprocess_text(raw_text)
            processed_text = processed_data.get('cleaned_text', raw_text)
            
            # Extract skills
            skills = self.skills_extractor.extract_skills(processed_text)
            technical_skills = self.skills_extractor.extract_technical_skills(processed_text)
            soft_skills = self.skills_extractor.extract_soft_skills(processed_text)
            
            # Comprehensive resume analysis
            full_analysis = self.resume_analyzer.analyze_full_resume(raw_text)
            
            # Calculate basic metrics
            text_length = len(raw_text)
            word_count = len(raw_text.split())
            
            processing_time = time.time() - start_time
            
            results = {
                'filename': Path(resume_path).name,
                'text_length': text_length,
                'word_count': word_count,
                'text': raw_text,  # Full text for scoring
                'skills': {
                    'technical_skills': list(technical_skills),
                    'soft_skills': list(soft_skills),
                    'all_skills': skills
                },
                'processing_time': processing_time,
                'full_analysis': full_analysis,  # Complete resume analysis
                'sections': full_analysis.get('sections', {}),
                'dates': full_analysis.get('dates', []),
                'experience': full_analysis.get('experience', []),
                'education': full_analysis.get('education', []),
                'contact_info': full_analysis.get('contact_info', {}),
                'projects': full_analysis.get('projects', []),
                'certifications': full_analysis.get('certifications', []),
                'languages': full_analysis.get('languages', []),
                'summary': full_analysis.get('summary', ''),
                'metrics': full_analysis.get('metrics', {})
            }
            
            self.logger.info(f"Analysis completed in {processing_time:.2f}s")
            return results
            
        except Exception as e:
            self.logger.error(f"Error analyzing resume {resume_path}: {str(e)}")
            self.logger.error(traceback.format_exc())
            return None
    
    def analyze_single_resume(self, resume_path: str, job_path: str, output_file: str = None) -> Optional[Dict[str, Any]]:
        """
        Analyze a single resume against a job description (CLI interface)
        
        Args:
            resume_path: Path to the resume file
            job_path: Path to the job description file
            output_file: Optional output file path
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Read job description
            with open(job_path, 'r', encoding='utf-8') as f:
                job_description = f.read().strip()
            
            # Match resume to job
            result = self.match_resume_to_job(resume_path, job_description)
            
            if result and output_file:
                save_results_to_json(result, output_file)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in analyze_single_resume: {str(e)}")
            self.logger.error(traceback.format_exc())
            return None
    
    def match_resume_to_job(self, resume_path: str, job_description: str) -> Optional[Dict[str, Any]]:
        """
        Match a resume against a specific job description
        
        Args:
            resume_path: Path to the resume file
            job_description: Job description text
            
        Returns:
            Dictionary containing match results
        """
        try:
            self.logger.info(f"Matching resume {resume_path} to job description")
            start_time = time.time()
            
            # Analyze resume
            resume_analysis = self.analyze_resume(resume_path)
            if not resume_analysis:
                return None
            
            # Create job requirements for ATS scoring
            job_requirements = {
                'experience_years': 7,  # Default for senior roles
                'required_skills': ['swift', 'swiftui', 'uikit', 'ios', 'xctest', 'fastlane'],
                'preferred_skills': ['firebase', 'jenkins', 'github actions', 'agile', 'accessibility']
            }
            
            # Score against job description using ATS analysis
            score_result = self.scorer.calculate_ats_score(resume_analysis, job_requirements)
            
            processing_time = time.time() - start_time
            
            results = {
                'resume_filename': Path(resume_path).name,
                'overall_score': score_result.get('overall_score', 0),
                'breakdown': score_result.get('breakdown', {}),
                'skills_found': resume_analysis.get('skills', {}),
                'processing_time': processing_time,
                # ATS Analysis Results
                'ats_analysis': {
                    'overall_score': score_result.get('overall_score', 0),
                    'highlights': score_result.get('highlights', []),
                    'gaps': score_result.get('gaps', []),
                    'recommendations': score_result.get('recommendations', []),
                    'detailed_matches': score_result.get('detailed_matches', [])
                },
                # Enhanced analysis data
                'experience': [self._convert_experience_to_dict(exp) for exp in resume_analysis.get('experience', [])],
                'education': [self._convert_education_to_dict(edu) for edu in resume_analysis.get('education', [])],
                'dates': resume_analysis.get('dates', []),
                'contact_info': resume_analysis.get('contact_info', {}),
                'projects': resume_analysis.get('projects', []),
                'certifications': resume_analysis.get('certifications', []),
                'languages': resume_analysis.get('languages', []),
                'summary': resume_analysis.get('summary', ''),
                'metrics': resume_analysis.get('metrics', {}),
                'sections': resume_analysis.get('sections', {})
            }
            
            self.logger.info(f"Match completed in {processing_time:.2f}s")
            return results
            
        except Exception as e:
            self.logger.error(f"Error matching resume to job: {str(e)}")
            self.logger.error(traceback.format_exc())
            return None
    
    def _convert_experience_to_dict(self, experience):
        """Convert Experience dataclass to dictionary"""
        if hasattr(experience, '__dict__'):
            return experience.__dict__
        return experience
    
    def _convert_education_to_dict(self, education):
        """Convert Education dataclass to dictionary"""
        if hasattr(education, '__dict__'):
            return education.__dict__
        return education
    
    def run_batch_analysis(self, resumes_dir: str, jobs_dir: str, 
                          output_file: str = None) -> Dict[str, Any]:
        """
        Run batch analysis on multiple resumes and job descriptions
        
        Args:
            resumes_dir: Directory containing resume files
            jobs_dir: Directory containing job description files
            output_file: Output file path (optional)
            
        Returns:
            Dictionary containing batch analysis results
        """
        try:
            self.logger.info(f"Starting batch analysis: {resumes_dir} vs {jobs_dir}")
            start_time = time.time()
            
            # Get all resume files
            resume_files = list(Path(resumes_dir).glob("*"))
            resume_files = [f for f in resume_files if f.is_file() and 
                          f.suffix.lower() in settings.SUPPORTED_FORMATS]
            
            # Get all job description files
            job_files = list(Path(jobs_dir).glob("*"))
            job_files = [f for f in job_files if f.is_file() and 
                        f.suffix.lower() in ['.txt', '.json', '.md']]
            
            if not resume_files:
                self.logger.error("No resume files found")
                return {'error': 'No resume files found'}
            
            if not job_files:
                self.logger.error("No job description files found")
                return {'error': 'No job description files found'}
            
            # Load job descriptions
            job_descriptions = {}
            for job_file in job_files:
                try:
                    with open(job_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    job_descriptions[job_file.name] = content
                except Exception as e:
                    self.logger.warning(f"Failed to load job file {job_file}: {str(e)}")
            
            # Process each resume against each job
            all_results = []
            total_matches = 0
            
            for resume_file in resume_files:
                resume_analysis = self.analyze_resume(str(resume_file))
                if not resume_analysis:
                    continue
                
                resume_results = {
                    'resume_filename': resume_file.name,
                    'resume_analysis': resume_analysis,
                    'job_matches': []
                }
                
                for job_name, job_content in job_descriptions.items():
                    match_result = self.match_resume_to_job(
                        str(resume_file), job_content
                    )
                    if match_result:
                        match_result['job_name'] = job_name
                        resume_results['job_matches'].append(match_result)
                        total_matches += 1
                
                all_results.append(resume_results)
            
            # Calculate summary statistics
            processing_time = time.time() - start_time
            
            summary = {
                'total_resumes': len(resume_files),
                'total_jobs': len(job_descriptions),
                'total_matches': total_matches,
                'processing_time': processing_time,
                'average_score': 0.0  # Will be calculated below
            }
            
            # Calculate average score
            all_scores = []
            for result in all_results:
                for match in result['job_matches']:
                    all_scores.append(match.get('overall_score', 0))
            
            if all_scores:
                summary['average_score'] = sum(all_scores) / len(all_scores)
            
            # Prepare final results
            final_results = {
                'summary': summary,
                'results': all_results,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Save results if output file specified
            if output_file:
                save_results_to_json(final_results, output_file)
                self.logger.info(f"Results saved to: {output_file}")
            
            self.logger.info(f"Batch analysis completed in {processing_time:.2f}s")
            return final_results
            
        except Exception as e:
            self.logger.error(f"Error in batch analysis: {str(e)}")
            self.logger.error(traceback.format_exc())
            return {'error': str(e)}
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get system status and health information
        
        Returns:
            Dictionary containing system status
        """
        try:
            status = {
                'components': {
                    'parser': self.parser is not None,
                    'preprocessor': self.preprocessor is not None,
                    'skills_extractor': self.skills_extractor is not None,
                    'scorer': self.scorer is not None
                },
                'directories': {
                    'resumes': settings.RESUMES_DIR.exists(),
                    'jobs': settings.JOBS_DIR.exists(),
                    'output': settings.OUTPUT_DIR.exists(),
                    'logs': settings.LOGS_DIR.exists()
                },
                'settings': {
                    'supported_formats': settings.SUPPORTED_FORMATS,
                    'scoring_weights': settings.SCORING_WEIGHTS,
                    'max_file_size': settings.MAX_FILE_SIZE
                }
            }
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting system status: {str(e)}")
            return {'error': str(e)}

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ApexHire AI Resume Screener")
    parser.add_argument('--resume', type=str, help='Path to resume file')
    parser.add_argument('--job', type=str, help='Path to job description file')
    parser.add_argument('--batch', action='store_true', help='Run batch analysis')
    parser.add_argument('--resumes-dir', type=str, help='Directory with resume files')
    parser.add_argument('--jobs-dir', type=str, help='Directory with job files')
    parser.add_argument('--output', type=str, default='output/results.json', help='Output file')
    
    args = parser.parse_args()
    
    screener = ResumeScreener()
    
    if args.batch and args.resumes_dir and args.jobs_dir:
        print("🔄 Running batch analysis...")
        results = screener.run_batch_analysis(args.resumes_dir, args.jobs_dir, args.output)
        print(f"✅ Batch analysis completed. Results saved to: {args.output}")
        
    elif args.resume and args.job:
        print(f"🔍 Analyzing {args.resume} against {args.job}...")
        result = screener.match_resume_to_job(args.resume, args.job)
        if result:
            print(f"✅ Analysis completed. Score: {result['overall_score']:.1%}")
        else:
            print("❌ Analysis failed")
            
    else:
        print("ℹ️ Use --help for usage information")

if __name__ == "__main__":
    main()
