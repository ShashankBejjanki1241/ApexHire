"""
Skills Extractor Module
Extracts skills, education, experience, and other entities from resume text
"""

import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SkillsExtractor:
    """Extract skills, education, experience, and other entities from resume text"""
    
    def __init__(self):
        # Common technical skills
        self.technical_skills = {
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'aws', 'azure', 'docker', 'kubernetes', 'git', 'sql', 'mongodb',
            'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn'
        }
        
        # Soft skills
        self.soft_skills = {
            'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
            'time management', 'project management', 'agile', 'scrum'
        }
    
    def extract_technical_skills(self, text: str):
        """Extract technical skills from text"""
        if not text:
            return set()
        
        text_lower = text.lower()
        found_skills = set()
        
        # Check for exact matches
        for skill in self.technical_skills:
            if skill in text_lower:
                found_skills.add(skill)
        
        logger.info(f"Extracted {len(found_skills)} technical skills")
        return found_skills
    
    def extract_soft_skills(self, text: str):
        """Extract soft skills from text"""
        if not text:
            return set()
        
        text_lower = text.lower()
        found_skills = set()
        
        # Check for exact matches
        for skill in self.soft_skills:
            if skill in text_lower:
                found_skills.add(skill)
        
        logger.info(f"Extracted {len(found_skills)} soft skills")
        return found_skills
    
    def extract_all_skills_and_info(self, text: str):
        """Extract all skills and information from resume text"""
        if not text:
            return {}
        
        results = {
            'technical_skills': list(self.extract_technical_skills(text)),
            'soft_skills': list(self.extract_soft_skills(text)),
            'education': {'degrees': [], 'institutions': [], 'years': []},
            'experience': {'companies': [], 'positions': [], 'durations': [], 'responsibilities': []},
            'entities': {}
        }
        
        # Calculate skill counts
        results['total_skills'] = len(results['technical_skills']) + len(results['soft_skills'])
        results['skill_breakdown'] = {
            'technical': len(results['technical_skills']),
            'soft': len(results['soft_skills'])
        }
        
        logger.info(f"Complete extraction: {results['total_skills']} total skills found")
        return results


if __name__ == "__main__":
    extractor = SkillsExtractor()
    print("Skills Extractor Module")
