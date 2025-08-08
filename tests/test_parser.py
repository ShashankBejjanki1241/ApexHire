"""
Test cases for the parser module
"""

import pytest
import tempfile
import os
from src.parser import ResumeParser

class TestResumeParser:
    """Test cases for ResumeParser class"""
    
    def test_supported_formats(self):
        """Test that supported formats are correctly identified"""
        parser = ResumeParser()
        assert '.pdf' in parser.supported_formats
        assert '.docx' in parser.supported_formats
        assert '.txt' in parser.supported_formats
    
    def test_parse_resume_with_invalid_file(self):
        """Test parsing with invalid file"""
        parser = ResumeParser()
        with tempfile.NamedTemporaryFile(suffix='.invalid', delete=False) as f:
            f.write(b"test content")
            f.flush()
            
            result = parser.parse_resume(f.name)
            assert result is None
            
        os.unlink(f.name)
    
    def test_extract_text_from_txt(self):
        """Test text extraction from TXT files"""
        parser = ResumeParser()
        test_content = "This is a test resume content."
        
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(test_content.encode('utf-8'))
            f.flush()
            
            result = parser.extract_text_from_txt(f.name)
            assert result == test_content
            
        os.unlink(f.name)

if __name__ == "__main__":
    pytest.main([__file__])
