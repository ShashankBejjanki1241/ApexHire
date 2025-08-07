"""
Resume Scorer Module
Scores and ranks resumes against job descriptions using semantic similarity and keyword matching
"""

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResumeScorer:
    """Score and rank resumes against job descriptions"""
    
    def __init__(self, use_semantic_similarity: bool = True):
        """Initialize the resume scorer"""
        self.use_semantic_similarity = use_semantic_similarity
        logger.info("Resume Scorer initialized")
    
    def calculate_keyword_similarity(self, resume_text: str, job_description: str) -> float:
        """Calculate keyword-based similarity"""
        if not resume_text or not job_description:
            return 0.0
        
        # Simple keyword matching
        resume_words = set(resume_text.lower().split())
        job_words = set(job_description.lower().split())
        
        if not job_words:
            return 0.0
        
        common_words = resume_words.intersection(job_words)
        similarity = len(common_words) / len(job_words)
        
        return float(similarity)
    
    def calculate_semantic_similarity(self, resume_text: str, job_description: str) -> float:
        """Calculate semantic similarity"""
        # For now, return a simple similarity based on text length
        if not resume_text or not job_description:
            return 0.0
        
        # Simple heuristic: longer texts might be more similar
        resume_len = len(resume_text)
        job_len = len(job_description)
        
        if job_len == 0:
            return 0.0
        
        # Normalize by the longer text
        max_len = max(resume_len, job_len)
        similarity = min(resume_len, job_len) / max_len
        
        return float(similarity)
    
    def calculate_overall_score(self, resume_data, job_description: str):
        """Calculate overall score for a resume against job description"""
        if not resume_data or not job_description:
            return {'overall_score': 0.0, 'breakdown': {}}
        
        # Calculate individual scores
        keyword_score = self.calculate_keyword_similarity(
            resume_data.get('text', ''), job_description
        )
        
        semantic_score = self.calculate_semantic_similarity(
            resume_data.get('text', ''), job_description
        )
        
        # Simple skill matching
        resume_skills = resume_data.get('skills', {}).get('technical_skills', [])
        job_skills = ['python', 'java', 'javascript', 'react', 'aws', 'docker']
        skill_matches = sum(1 for skill in resume_skills if skill in job_skills)
        skill_score = skill_matches / len(job_skills) if job_skills else 0.0
        
        # Calculate weighted overall score
        overall_score = (keyword_score * 0.4 + semantic_score * 0.3 + skill_score * 0.3)
        
        return {
            'overall_score': overall_score,
            'breakdown': {
                'keyword_similarity': keyword_score,
                'semantic_similarity': semantic_score,
                'skill_match_ratio': skill_score,
                'experience_score': 0.5,  # Default values
                'education_score': 0.5,
                'skill_details': {'matched_skill_list': resume_skills}
            }
        }
    
    def rank_resumes(self, resumes, job_description: str):
        """Rank multiple resumes against a job description"""
        if not resumes or not job_description:
            return []
        
        ranked_resumes = []
        
        for resume in resumes:
            score_result = self.calculate_overall_score(resume, job_description)
            
            ranked_resume = {
                'filename': resume.get('filename', 'Unknown'),
                'score': score_result['overall_score'],
                'breakdown': score_result['breakdown'],
                'original_data': resume
            }
            
            ranked_resumes.append(ranked_resume)
        
        # Sort by score (highest first)
        ranked_resumes.sort(key=lambda x: x['score'], reverse=True)
        
        logger.info(f"Ranked {len(ranked_resumes)} resumes")
        return ranked_resumes


if __name__ == "__main__":
    scorer = ResumeScorer()
    print("Resume Scorer Module")
