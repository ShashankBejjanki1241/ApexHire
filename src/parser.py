"""
Resume Parser Module
Extracts text from PDF and DOCX resume files
"""

import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResumeParser:
    """Parser for extracting text from resume files (PDF and DOCX)"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.doc']
    
    def parse_resume(self, file_path: str):
        """Parse a resume file and extract text"""
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return {}
        
        filename = os.path.basename(file_path)
        
        # For now, just return basic info
        return {
            'filename': filename,
            'text': f"Sample text from {filename}",
            'file_path': file_path
        }
    
    def parse_multiple_resumes(self, directory_path: str):
        """Parse multiple resume files from a directory"""
        parsed_resumes = []
        
        if not os.path.exists(directory_path):
            logger.error(f"Directory not found: {directory_path}")
            return parsed_resumes
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            if os.path.isfile(file_path):
                file_extension = os.path.splitext(filename)[1].lower()
                
                if file_extension in self.supported_formats:
                    parsed_resume = self.parse_resume(file_path)
                    if parsed_resume:
                        parsed_resumes.append(parsed_resume)
        
        logger.info(f"Successfully parsed {len(parsed_resumes)} resume files")
        return parsed_resumes


if __name__ == "__main__":
    parser = ResumeParser()
    print("Resume Parser Module")
