"""
Advanced ATS Resume Scorer Module
Provides comprehensive ATS-style analysis with detailed breakdowns, recommendations, and insights
"""

import logging
from typing import Dict, List, Any, Set
import re
from datetime import datetime
import fuzzywuzzy.fuzz as fuzz

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResumeScorer:
    """Advanced ATS Resume Scorer with detailed analysis"""
    
    def __init__(self, use_semantic_similarity: bool = True):
        """Initialize the resume scorer"""
        self.use_semantic_similarity = use_semantic_similarity
        logger.info("Advanced ATS Resume Scorer initialized")
    
    def calculate_ats_score(self, resume_analysis: Dict[str, Any], 
                          job_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive ATS match score with detailed breakdown"""
        
        # Extract key data
        resume_skills = resume_analysis.get('skills', resume_analysis.get('skills_found', {}))
        technical_skills = set(resume_skills.get('technical_skills', []))
        soft_skills = set(resume_skills.get('soft_skills', []))
        experience_entries = resume_analysis.get('experience', [])
        education_entries = resume_analysis.get('education', [])
        
        # Debug logging
        logger.info(f"Technical skills found: {len(technical_skills)}")
        logger.info(f"Soft skills found: {len(soft_skills)}")
        logger.info(f"Experience entries: {len(experience_entries)}")
        
        # Calculate detailed breakdown
        breakdown = self._calculate_detailed_breakdown(
            technical_skills, soft_skills, experience_entries, 
            education_entries, job_requirements
        )
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(breakdown)
        
        # Generate comprehensive analysis
        analysis = {
            'overall_score': overall_score,
            'breakdown': breakdown,
            'highlights': self._identify_highlights(resume_analysis),
            'gaps': self._identify_gaps(breakdown, job_requirements),
            'recommendations': self._generate_recommendations(breakdown, resume_analysis),
            'detailed_matches': self._create_detailed_matches(breakdown, job_requirements)
        }
        
        return analysis
    
    def _calculate_detailed_breakdown(self, technical_skills: Set[str], 
                                    soft_skills: Set[str],
                                    experience_entries: List[Dict],
                                    education_entries: List[Dict],
                                    job_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate detailed breakdown of all matching criteria"""
        
        # Experience analysis
        total_experience = self._calculate_total_experience(experience_entries)
        required_years = job_requirements.get('experience_years', 0)
        experience_score = min((total_experience / required_years) * 100, 100) if required_years > 0 else 100
        
        # Skill analysis
        required_skills = set(job_requirements.get('required_skills', []))
        preferred_skills = set(job_requirements.get('preferred_skills', []))
        
        required_matches = len(technical_skills.intersection(required_skills))
        preferred_matches = len(technical_skills.intersection(preferred_skills))
        
        required_score = (required_matches / len(required_skills)) * 100 if required_skills else 0
        preferred_score = (preferred_matches / len(preferred_skills)) * 100 if preferred_skills else 0
        
        # Specific requirement checks
        specific_checks = self._check_specific_requirements(technical_skills, soft_skills, experience_entries)
        
        return {
            'experience': {
                'total_years': total_experience,
                'required_years': required_years,
                'score': experience_score,
                'status': self._get_experience_status(total_experience, required_years)
            },
            'skills': {
                'required_matches': required_matches,
                'preferred_matches': preferred_matches,
                'total_required': len(required_skills),
                'total_preferred': len(preferred_skills),
                'required_score': required_score,
                'preferred_score': preferred_score,
                'total_skills_found': len(technical_skills)
            },
            'specific_requirements': specific_checks
        }
    
    def _calculate_total_experience(self, experience_entries: List[Dict]) -> float:
        """Calculate total years of experience from resume"""
        total_years = 0.0
        
        for exp in experience_entries:
            # Handle both dictionary and dataclass objects
            if hasattr(exp, 'start_date'):
                start_date = exp.start_date
                end_date = exp.end_date
            else:
                start_date = exp.get('start_date', '')
                end_date = exp.get('end_date', '')
            
            if start_date and end_date:
                try:
                    # Extract year from dates like "Jul 2023" or "2023"
                    start_year = self._extract_year(str(start_date))
                    end_year = self._extract_year(str(end_date))
                    
                    if start_year and end_year:
                        years = end_year - start_year
                        # Add partial years if months are specified
                        if 'present' in str(end_date).lower() or 'current' in str(end_date).lower():
                            years += 0.5  # Assume current year
                        total_years += years
                except:
                    pass
        
        return total_years
    
    def _extract_year(self, date_str: str) -> int:
        """Extract year from date string"""
        # Look for 4-digit year
        year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
        if year_match:
            return int(year_match.group())
        return None
    
    def _get_experience_status(self, actual_years: float, required_years: float) -> str:
        """Get status for experience requirement"""
        if actual_years >= required_years:
            return "✅ Yes"
        elif actual_years >= required_years * 0.8:  # Within 20%
            return "⚠️ Partial"
        else:
            return "❌ No"
    
    def _check_specific_requirements(self, technical_skills: Set[str], 
                                   soft_skills: Set[str],
                                   experience_entries: List[Dict]) -> Dict[str, Any]:
        """Check specific job requirements"""
        
        # Convert technical_skills to lowercase for comparison
        technical_skills_lower = {skill.lower() for skill in technical_skills}
        soft_skills_lower = {skill.lower() for skill in soft_skills}
        
        # iOS Development
        ios_skills = {'swift', 'swiftui', 'uikit', 'cocoa touch', 'ios'}
        ios_development = any(skill.lower() in technical_skills_lower for skill in ios_skills)
        
        # Swift Experience
        swift_experience = any(skill.lower() in technical_skills_lower for skill in ['swift', 'swiftui'])
        
        # Team Collaboration
        collaboration_skills = {'agile', 'scrum', 'collaboration', 'team'}
        team_collaboration = any(skill.lower() in soft_skills_lower for skill in collaboration_skills)
        
        # Accessibility
        accessibility_skills = {'accessibility', 'voiceover', 'wcag', 'dynamic type'}
        accessibility = any(skill.lower() in technical_skills_lower for skill in accessibility_skills)
        
        # Testing
        testing_skills = {'xctest', 'xcuitest', 'testing', 'tdd', 'unit testing'}
        testing = any(skill.lower() in technical_skills_lower for skill in testing_skills)
        
        # CI/CD
        cicd_skills = {'jenkins', 'fastlane', 'github actions', 'ci/cd', 'bitrise'}
        cicd = any(skill.lower() in technical_skills_lower for skill in cicd_skills)
        
        # Authentication
        auth_skills = {'oauth', 'oauth 2.0', 'authentication', 'jwt'}
        authentication = any(skill.lower() in technical_skills_lower for skill in auth_skills)
        
        # App Store
        appstore_skills = {'app store connect', 'testflight', 'app store'}
        app_store = any(skill.lower() in technical_skills_lower for skill in appstore_skills)
        
        # Education
        has_degree = len(experience_entries) > 0  # Simplified check
        
        return {
            'ios_development': {'status': "✅ Yes" if ios_development else "❌ No", 'details': "Strong iOS skills found" if ios_development else "iOS skills not prominent"},
            'swift_experience': {'status': "✅ Yes" if swift_experience else "❌ No", 'details': "Swift/SwiftUI experience confirmed" if swift_experience else "Swift experience not found"},
            'team_collaboration': {'status': "✅ Yes" if team_collaboration else "❌ No", 'details': "Team collaboration skills present" if team_collaboration else "Team skills not mentioned"},
            'accessibility': {'status': "✅ Yes" if accessibility else "❌ No", 'details': "Accessibility experience found" if accessibility else "Accessibility not mentioned"},
            'testing': {'status': "✅ Yes" if testing else "❌ No", 'details': "Testing experience confirmed" if testing else "Testing experience not found"},
            'cicd': {'status': "✅ Yes" if cicd else "❌ No", 'details': "CI/CD experience present" if cicd else "CI/CD not mentioned"},
            'authentication': {'status': "✅ Yes" if authentication else "❌ No", 'details': "Authentication experience found" if authentication else "Auth experience not found"},
            'app_store': {'status': "✅ Yes" if app_store else "❌ No", 'details': "App Store experience confirmed" if app_store else "App Store experience not found"},
            'education': {'status': "✅ Yes" if has_degree else "❌ No", 'details': "Education requirements met" if has_degree else "Education requirements not met"}
        }
    
    def _calculate_overall_score(self, breakdown: Dict[str, Any]) -> float:
        """Calculate overall ATS score"""
        
        # Weighted scoring
        experience_weight = 0.25
        skills_weight = 0.35
        specific_weight = 0.40
        
        # Experience score
        experience_score = breakdown['experience']['score'] * experience_weight
        
        # Skills score
        skills_score = (breakdown['skills']['required_score'] * 0.7 + 
                      breakdown['skills']['preferred_score'] * 0.3) * skills_weight
        
        # Specific requirements score
        specific_checks = breakdown['specific_requirements']
        specific_passed = sum(1 for check in specific_checks.values() 
                            if "✅ Yes" in check['status'])
        specific_score = (specific_passed / len(specific_checks)) * 100 * specific_weight
        
        overall_score = experience_score + skills_score + specific_score
        
        return min(overall_score, 100)
    
    def _identify_highlights(self, resume_analysis: Dict[str, Any]) -> List[str]:
        """Identify key highlights from the resume"""
        highlights = []
        
        # Experience highlights
        experience = resume_analysis.get('experience', [])
        if experience:
            highlights.append(f"Strong experience with {len(experience)} professional roles")
        
        # Skills highlights
        skills = resume_analysis.get('skills_found', {})
        tech_skills = skills.get('technical_skills', [])
        if len(tech_skills) > 50:
            highlights.append(f"Comprehensive technical skill set ({len(tech_skills)} skills identified)")
        
        # Specific technology highlights
        if any('swift' in skill.lower() for skill in tech_skills):
            highlights.append("Expert Swift and iOS development experience")
        
        if any('firebase' in skill.lower() for skill in tech_skills):
            highlights.append("Strong Firebase and cloud integration experience")
        
        if any('agile' in skill.lower() for skill in tech_skills):
            highlights.append("Agile methodology and team collaboration experience")
        
        if any('accessibility' in skill.lower() for skill in tech_skills):
            highlights.append("Accessibility and inclusive design experience")
        
        if any('testing' in skill.lower() for skill in tech_skills):
            highlights.append("Comprehensive testing and quality assurance experience")
        
        return highlights
    
    def _identify_gaps(self, breakdown: Dict[str, Any], job_requirements: Dict[str, Any]) -> List[str]:
        """Identify gaps between resume and job requirements"""
        gaps = []
        
        # Experience gaps
        experience = breakdown['experience']
        if experience['total_years'] < experience['required_years']:
            gap_years = experience['required_years'] - experience['total_years']
            gaps.append(f"Experience: {experience['total_years']} years vs required {experience['required_years']} years (gap: {gap_years} years)")
        
        # Skills gaps
        skills = breakdown['skills']
        if skills['required_score'] < 80:
            gaps.append(f"Required skills match: {skills['required_score']:.1f}% (target: 80%+)")
        
        # Specific requirement gaps
        specific_checks = breakdown['specific_requirements']
        failed_checks = [name for name, check in specific_checks.items() 
                        if "❌ No" in check['status']]
        
        for failed in failed_checks:
            gaps.append(f"Missing: {failed.replace('_', ' ').title()}")
        
        return gaps
    
    def _generate_recommendations(self, breakdown: Dict[str, Any], resume_analysis: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations for improvement"""
        recommendations = []
        
        # Experience recommendations
        experience = breakdown['experience']
        if experience['total_years'] < experience['required_years']:
            gap_years = experience['required_years'] - experience['total_years']
            recommendations.append(f"Add {gap_years} more years of experience or highlight relevant projects/freelance work")
        
        # Skills recommendations
        skills = breakdown['skills']
        if skills['required_score'] < 80:
            recommendations.append("Add more required technical skills to your resume")
        
        # Specific recommendations
        specific_checks = breakdown['specific_requirements']
        
        if "❌ No" in specific_checks.get('accessibility', {}).get('status', ''):
            recommendations.append("Include accessibility experience (VoiceOver, WCAG compliance, Dynamic Type)")
        
        if "❌ No" in specific_checks.get('testing', {}).get('status', ''):
            recommendations.append("Highlight testing experience (XCTest, XCUITest, TDD, automated testing)")
        
        if "❌ No" in specific_checks.get('cicd', {}).get('status', ''):
            recommendations.append("Add CI/CD experience (Jenkins, Fastlane, GitHub Actions, automated deployment)")
        
        if "❌ No" in specific_checks.get('team_collaboration', {}).get('status', ''):
            recommendations.append("Emphasize team collaboration and Agile methodology experience")
        
        return recommendations
    
    def _create_detailed_matches(self, breakdown: Dict[str, Any], job_requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create detailed match breakdown for display with explanations"""
        matches = []
        
        # Experience match
        experience = breakdown['experience']
        matches.append({
            'requirement': f"{experience['required_years']}+ years experience",
            'matched': experience['status'],
            'details': f"Resume shows {experience['total_years']} years experience",
            'confidence': self._calculate_experience_confidence(experience),
            'explanation': self._explain_experience_match(experience)
        })
        
        # Skills match
        skills = breakdown['skills']
        matches.append({
            'requirement': "Required technical skills",
            'matched': f"{skills['required_matches']}/{skills['total_required']} matched",
            'details': f"Match rate: {skills['required_score']:.1f}%",
            'confidence': skills['required_score'] / 100.0,
            'explanation': self._explain_skills_match(skills)
        })
        
        # Specific requirements with detailed explanations
        specific_checks = breakdown['specific_requirements']
        for req_name, check in specific_checks.items():
            matches.append({
                'requirement': req_name.replace('_', ' ').title(),
                'matched': check['status'],
                'details': check['details'],
                'confidence': 1.0 if "✅ Yes" in check['status'] else 0.0,
                'explanation': self._explain_specific_requirement(req_name, check)
            })
        
        return matches
    
    def _calculate_experience_confidence(self, experience: Dict[str, Any]) -> float:
        """Calculate confidence level for experience match"""
        actual_years = experience['total_years']
        required_years = experience['required_years']
        
        if actual_years >= required_years:
            return 1.0
        elif actual_years >= required_years * 0.8:
            return 0.8
        elif actual_years >= required_years * 0.6:
            return 0.6
        else:
            return 0.3
    
    def _explain_experience_match(self, experience: Dict[str, Any]) -> str:
        """Explain the experience match"""
        actual_years = experience['total_years']
        required_years = experience['required_years']
        
        if actual_years >= required_years:
            return f"✅ Excellent! {actual_years} years exceeds the {required_years} year requirement."
        elif actual_years >= required_years * 0.8:
            return f"⚠️ Close match: {actual_years} years is {required_years - actual_years} years short of {required_years} required."
        else:
            return f"❌ Significant gap: {actual_years} years is {required_years - actual_years} years short of {required_years} required."
    
    def _explain_skills_match(self, skills: Dict[str, Any]) -> str:
        """Explain the skills match"""
        required_matches = skills['required_matches']
        total_required = skills['total_required']
        required_score = skills['required_score']
        
        if required_score >= 90:
            return f"✅ Excellent skills match! {required_matches}/{total_required} required skills found."
        elif required_score >= 70:
            return f"👍 Good skills match: {required_matches}/{total_required} required skills found."
        elif required_score >= 50:
            return f"⚠️ Moderate skills match: {required_matches}/{total_required} required skills found."
        else:
            return f"❌ Limited skills match: {required_matches}/{total_required} required skills found."
    
    def _explain_specific_requirement(self, req_name: str, check: Dict[str, Any]) -> str:
        """Explain specific requirement match"""
        status = check['status']
        details = check['details']
        
        if "✅ Yes" in status:
            return f"✅ Strong evidence found: {details}"
        elif "⚠️ Partial" in status:
            return f"⚠️ Partial evidence: {details}"
        else:
            return f"❌ No evidence found: {details}"
    
    def generate_skill_breakdown(self, resume_skills: Set[str], job_skills: List[str]) -> Dict[str, Any]:
        """Generate detailed skill breakdown with explanations"""
        breakdown = {
            'matched_skills': [],
            'missing_skills': [],
            'partial_matches': [],
            'confidence_scores': {}
        }
        
        for job_skill in job_skills:
            # Check for exact matches
            if job_skill.lower() in {skill.lower() for skill in resume_skills}:
                breakdown['matched_skills'].append({
                    'skill': job_skill,
                    'confidence': 1.0,
                    'match_type': 'exact',
                    'explanation': f"✅ Exact match found for '{job_skill}'"
                })
                breakdown['confidence_scores'][job_skill] = 1.0
            else:
                # Check for fuzzy matches
                best_match = None
                best_score = 0
                
                for resume_skill in resume_skills:
                    score = fuzz.ratio(job_skill.lower(), resume_skill.lower())
                    if score > best_score and score >= 70:
                        best_score = score
                        best_match = resume_skill
                
                if best_match:
                    breakdown['partial_matches'].append({
                        'required_skill': job_skill,
                        'found_skill': best_match,
                        'confidence': best_score / 100.0,
                        'match_type': 'fuzzy',
                        'explanation': f"⚠️ Partial match: '{job_skill}' similar to '{best_match}' ({best_score}% similarity)"
                    })
                    breakdown['confidence_scores'][job_skill] = best_score / 100.0
                else:
                    breakdown['missing_skills'].append({
                        'skill': job_skill,
                        'confidence': 0.0,
                        'match_type': 'missing',
                        'explanation': f"❌ No match found for '{job_skill}'"
                    })
                    breakdown['confidence_scores'][job_skill] = 0.0
        
        return breakdown


if __name__ == "__main__":
    scorer = ResumeScorer()
    print("Advanced ATS Resume Scorer Module")
