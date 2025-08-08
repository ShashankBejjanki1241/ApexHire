"""
Enhanced Resume Analyzer
Extracts comprehensive information from resumes including dates, experience, education, and full content analysis
"""

import re
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Experience:
    company: str
    position: str
    start_date: Optional[str]
    end_date: Optional[str]
    duration: Optional[str]
    responsibilities: List[str]
    technologies: List[str]

@dataclass
class Education:
    institution: str
    degree: str
    field: str
    start_date: Optional[str]
    end_date: Optional[str]
    gpa: Optional[str]

class ResumeAnalyzer:
    """Comprehensive resume analyzer that extracts detailed information"""
    
    def __init__(self):
        # Date patterns
        self.date_patterns = [
            r'(\w{3}\s+\d{4})\s*[-–]\s*(\w{3}\s+\d{4}|\bPresent\b|\bCurrent\b)',  # Jan 2020 - Present
            r'(\d{1,2}/\d{1,2}/\d{4})\s*[-–]\s*(\d{1,2}/\d{1,2}/\d{4}|\bPresent\b)',  # 01/2020 - Present
            r'(\d{4})\s*[-–]\s*(\d{4}|\bPresent\b)',  # 2020 - Present
            r'(\w+\s+\d{4})\s*[-–]\s*(\w+\s+\d{4}|\bPresent\b)',  # January 2020 - Present
        ]
        
        # Experience section patterns
        self.experience_patterns = [
            r'(?:EXPERIENCE|WORK EXPERIENCE|PROFESSIONAL EXPERIENCE|EMPLOYMENT HISTORY)',
            r'(?:Client|Company|Employer):\s*([^,\n]+)',
            r'(?:Role|Position|Title):\s*([^,\n]+)',
            r'(?:Responsibilities|Duties|Key Achievements):',
        ]
        
        # Education patterns
        self.education_patterns = [
            r'(?:EDUCATION|ACADEMIC|DEGREES)',
            r'(?:University|College|School|Institute):\s*([^,\n]+)',
            r'(?:Degree|Bachelor|Master|PhD):\s*([^,\n]+)',
            r'(?:GPA|Grade):\s*([\d.]+)',
        ]
        
        # Technology patterns
        self.tech_patterns = [
            r'(?:Technologies|Tools|Frameworks|Languages):\s*([^.\n]+)',
            r'(?:Environments|Platforms):\s*([^.\n]+)',
        ]
    
    def analyze_full_resume(self, text: str) -> Dict[str, Any]:
        """Analyze the complete resume and extract comprehensive information"""
        if not text:
            return {}
        
        analysis = {
            'full_text': text,
            'text_length': len(text),
            'word_count': len(text.split()),
            'sections': self._extract_sections(text),
            'dates': self._extract_dates(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'contact_info': self._extract_contact_info(text),
            'skills_sections': self._extract_skills_sections(text),
            'summary': self._extract_summary(text),
            'projects': self._extract_projects(text),
            'certifications': self._extract_certifications(text),
            'languages': self._extract_languages(text),
            'metrics': self._calculate_metrics(text)
        }
        
        logger.info(f"Comprehensive analysis completed: {len(text)} characters, {analysis['word_count']} words")
        return analysis
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections of the resume"""
        sections = {}
        
        # Common section headers
        section_headers = [
            'PROFESSIONAL SUMMARY', 'SUMMARY', 'OBJECTIVE',
            'EXPERIENCE', 'WORK EXPERIENCE', 'EMPLOYMENT HISTORY',
            'EDUCATION', 'ACADEMIC BACKGROUND',
            'SKILLS', 'TECHNICAL SKILLS', 'COMPETENCIES',
            'PROJECTS', 'PORTFOLIO',
            'CERTIFICATIONS', 'CERTIFICATES',
            'LANGUAGES', 'LANGUAGE SKILLS'
        ]
        
        lines = text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line_upper = line.strip().upper()
            
            # Check if this line is a section header
            is_header = any(header in line_upper for header in section_headers)
            
            if is_header:
                # Save previous section
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = line.strip()
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Save last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def _extract_dates(self, text: str) -> List[Dict[str, str]]:
        """Extract all dates from the resume"""
        dates = []
        
        for pattern in self.date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                start_date = match.group(1).strip()
                end_date = match.group(2).strip()
                
                dates.append({
                    'start_date': start_date,
                    'end_date': end_date,
                    'full_match': match.group(0),
                    'pattern_used': pattern
                })
        
        return dates
    
    def _extract_experience(self, text: str) -> List[Experience]:
        """Extract work experience information"""
        experiences = []
        
        # Look for experience sections
        experience_sections = re.findall(r'(?:EXPERIENCE|WORK EXPERIENCE|EMPLOYMENT HISTORY).*?(?=\n\n|\Z)', 
                                       text, re.IGNORECASE | re.DOTALL)
        
        for section in experience_sections:
            # Extract company and position
            company_match = re.search(r'(?:Client|Company|Employer):\s*([^,\n]+)', section, re.IGNORECASE)
            position_match = re.search(r'(?:Role|Position|Title):\s*([^,\n]+)', section, re.IGNORECASE)
            
            if company_match:
                company = company_match.group(1).strip()
                position = position_match.group(1).strip() if position_match else "Unknown"
                
                # Extract dates
                dates = self._extract_dates(section)
                start_date = dates[0]['start_date'] if dates else None
                end_date = dates[0]['end_date'] if dates else None
                
                # Extract responsibilities
                responsibilities = []
                resp_section = re.search(r'(?:Responsibilities|Duties|Key Achievements):(.*?)(?=\n\n|\Z)', 
                                       section, re.IGNORECASE | re.DOTALL)
                if resp_section:
                    resp_text = resp_section.group(1)
                    responsibilities = [line.strip() for line in resp_text.split('\n') if line.strip()]
                
                # Extract technologies
                technologies = []
                tech_section = re.search(r'(?:Technologies|Tools|Frameworks|Environments):(.*?)(?=\n\n|\Z)', 
                                       section, re.IGNORECASE | re.DOTALL)
                if tech_section:
                    tech_text = tech_section.group(1)
                    technologies = [tech.strip() for tech in tech_text.split(',') if tech.strip()]
                
                experience = Experience(
                    company=company,
                    position=position,
                    start_date=start_date,
                    end_date=end_date,
                    duration=self._calculate_duration(start_date, end_date),
                    responsibilities=responsibilities,
                    technologies=technologies
                )
                experiences.append(experience)
        
        return experiences
    
    def _extract_education(self, text: str) -> List[Education]:
        """Extract education information"""
        education_list = []
        
        # Look for education sections
        education_sections = re.findall(r'(?:EDUCATION|ACADEMIC BACKGROUND).*?(?=\n\n|\Z)', 
                                      text, re.IGNORECASE | re.DOTALL)
        
        for section in education_sections:
            # Extract institution
            institution_match = re.search(r'(?:University|College|School|Institute):\s*([^,\n]+)', 
                                       section, re.IGNORECASE)
            
            if institution_match:
                institution = institution_match.group(1).strip()
                
                # Extract degree
                degree_match = re.search(r'(?:Degree|Bachelor|Master|PhD):\s*([^,\n]+)', 
                                       section, re.IGNORECASE)
                degree = degree_match.group(1).strip() if degree_match else "Unknown"
                
                # Extract field
                field_match = re.search(r'(?:in|of)\s+([^,\n]+)', degree, re.IGNORECASE)
                field = field_match.group(1).strip() if field_match else "Unknown"
                
                # Extract dates
                dates = self._extract_dates(section)
                start_date = dates[0]['start_date'] if dates else None
                end_date = dates[0]['end_date'] if dates else None
                
                # Extract GPA
                gpa_match = re.search(r'(?:GPA|Grade):\s*([\d.]+)', section, re.IGNORECASE)
                gpa = gpa_match.group(1) if gpa_match else None
                
                education = Education(
                    institution=institution,
                    degree=degree,
                    field=field,
                    start_date=start_date,
                    end_date=end_date,
                    gpa=gpa
                )
                education_list.append(education)
        
        return education_list
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information"""
        contact_info = {}
        
        # Email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        if email_match:
            contact_info['email'] = email_match.group(0)
        
        # Phone
        phone_match = re.search(r'[\+]?[1-9][\d]{0,15}', text)
        if phone_match:
            contact_info['phone'] = phone_match.group(0)
        
        # LinkedIn
        linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', text, re.IGNORECASE)
        if linkedin_match:
            contact_info['linkedin'] = linkedin_match.group(0)
        
        # GitHub
        github_match = re.search(r'github\.com/[\w-]+', text, re.IGNORECASE)
        if github_match:
            contact_info['github'] = github_match.group(0)
        
        return contact_info
    
    def _extract_skills_sections(self, text: str) -> Dict[str, List[str]]:
        """Extract skills from different sections"""
        skills_sections = {}
        
        # Look for skills sections
        skills_patterns = [
            r'(?:TECHNICAL SKILLS|TECHNOLOGIES).*?(?=\n\n|\Z)',
            r'(?:PROGRAMMING LANGUAGES).*?(?=\n\n|\Z)',
            r'(?:FRAMEWORKS|LIBRARIES).*?(?=\n\n|\Z)',
            r'(?:TOOLS|PLATFORMS).*?(?=\n\n|\Z)',
        ]
        
        for pattern in skills_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Extract skills from the section
                skills = []
                lines = match.split('\n')
                for line in lines:
                    if ':' in line:
                        skill_part = line.split(':')[1]
                        skills.extend([skill.strip() for skill in skill_part.split(',')])
                    else:
                        skills.extend([skill.strip() for skill in line.split(',')])
                
                skills = [skill for skill in skills if skill and len(skill) > 1]
                if skills:
                    section_name = pattern.split('|')[0].replace('(', '').replace(')', '').strip()
                    skills_sections[section_name] = skills
        
        return skills_sections
    
    def _extract_summary(self, text: str) -> str:
        """Extract professional summary"""
        summary_patterns = [
            r'(?:PROFESSIONAL SUMMARY|SUMMARY|OBJECTIVE).*?(?=\n\n|\Z)',
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(0).strip()
        
        return ""
    
    def _extract_projects(self, text: str) -> List[Dict[str, str]]:
        """Extract project information"""
        projects = []
        
        project_sections = re.findall(r'(?:PROJECTS|PORTFOLIO).*?(?=\n\n|\Z)', 
                                    text, re.IGNORECASE | re.DOTALL)
        
        for section in project_sections:
            # Extract project names and descriptions
            project_matches = re.findall(r'([^:]+):\s*([^.\n]+)', section)
            for name, description in project_matches:
                projects.append({
                    'name': name.strip(),
                    'description': description.strip()
                })
        
        return projects
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        certifications = []
        
        cert_sections = re.findall(r'(?:CERTIFICATIONS|CERTIFICATES).*?(?=\n\n|\Z)', 
                                 text, re.IGNORECASE | re.DOTALL)
        
        for section in cert_sections:
            # Extract certification names
            cert_matches = re.findall(r'([^,\n]+)', section)
            for cert in cert_matches:
                cert_clean = cert.strip()
                if cert_clean and len(cert_clean) > 3:
                    certifications.append(cert_clean)
        
        return certifications
    
    def _extract_languages(self, text: str) -> List[str]:
        """Extract language skills"""
        languages = []
        
        lang_sections = re.findall(r'(?:LANGUAGES|LANGUAGE SKILLS).*?(?=\n\n|\Z)', 
                                 text, re.IGNORECASE | re.DOTALL)
        
        for section in lang_sections:
            # Extract languages
            lang_matches = re.findall(r'([^,\n]+)', section)
            for lang in lang_matches:
                lang_clean = lang.strip()
                if lang_clean and len(lang_clean) > 2:
                    languages.append(lang_clean)
        
        return languages
    
    def _calculate_duration(self, start_date: Optional[str], end_date: Optional[str]) -> Optional[str]:
        """Calculate duration between dates"""
        if not start_date or not end_date:
            return None
        
        try:
            # Parse dates (simplified)
            if 'Present' in end_date or 'Current' in end_date:
                return f"From {start_date} to Present"
            else:
                return f"{start_date} - {end_date}"
        except:
            return None
    
    def _calculate_metrics(self, text: str) -> Dict[str, Any]:
        """Calculate various metrics about the resume"""
        lines = text.split('\n')
        words = text.split()
        
        return {
            'total_lines': len(lines),
            'total_words': len(words),
            'total_characters': len(text),
            'average_words_per_line': len(words) / len(lines) if lines else 0,
            'sections_count': len(self._extract_sections(text)),
            'dates_count': len(self._extract_dates(text)),
            'experience_count': len(self._extract_experience(text)),
            'education_count': len(self._extract_education(text)),
            'projects_count': len(self._extract_projects(text)),
            'certifications_count': len(self._extract_certifications(text)),
            'languages_count': len(self._extract_languages(text))
        }
