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
        self.supported_formats = ['.pdf', '.docx', '.doc', '.txt']
    
    def parse_resume(self, file_path: str):
        """Parse a resume file and extract text"""
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None
        
        filename = os.path.basename(file_path)
        file_extension = os.path.splitext(filename)[1].lower()
        
        try:
            if file_extension == '.pdf':
                return self._parse_pdf(file_path)
            elif file_extension in ['.docx', '.doc']:
                return self._parse_docx(file_path)
            elif file_extension == '.txt':
                return self._parse_txt(file_path)
            else:
                logger.error(f"Unsupported file format: {file_extension}")
                return None
                
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {str(e)}")
            return None
    
    def _parse_pdf(self, file_path: str) -> str:
        """Parse PDF file and extract text"""
        try:
            import pdfplumber
            
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            logger.info(f"Successfully parsed PDF: {file_path}")
            return text.strip()
            
        except ImportError:
            logger.error("pdfplumber not installed. Please install it: pip install pdfplumber")
            return None
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {str(e)}")
            return None
    
    def _parse_docx(self, file_path: str) -> str:
        """Parse DOCX file and extract text"""
        try:
            from docx import Document
            
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            logger.info(f"Successfully parsed DOCX: {file_path}")
            return text.strip()
            
        except ImportError:
            logger.error("python-docx not installed. Please install it: pip install python-docx")
            return None
        except Exception as e:
            logger.error(f"Error parsing DOCX {file_path}: {str(e)}")
            return None
    
    def _parse_txt(self, file_path: str) -> str:
        """Parse TXT file and extract text"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            logger.info(f"Successfully parsed TXT: {file_path}")
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error parsing TXT {file_path}: {str(e)}")
            return None
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file (alias for _parse_txt)"""
        return self._parse_txt(file_path)
    
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
