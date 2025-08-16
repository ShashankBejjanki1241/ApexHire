"""
Text Preprocessing Module
Cleans and tokenizes resume text for NLP processing
"""

import re
import logging

# Import centralized logging
from utils import setup_logging
logger = logging.getLogger(__name__)


class TextPreprocessor:
    """Text preprocessing for resume analysis"""
    
    def __init__(self):
        self.stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        logger.info(f"Cleaned text, length: {len(text)} characters")
        return text
    
    def preprocess_text(self, text: str):
        """Complete text preprocessing pipeline"""
        if not text:
            return {
                'original_text': "",
                'cleaned_text': "",
                'tokens': [],
                'sentences': [],
                'processed_tokens': []
            }
        
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Simple tokenization
        tokens = cleaned_text.split()
        
        # Remove stop words
        processed_tokens = [token for token in tokens if token not in self.stop_words]
        
        return {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'tokens': tokens,
            'sentences': [cleaned_text],
            'processed_tokens': processed_tokens
        }


if __name__ == "__main__":
    preprocessor = TextPreprocessor()
    print("Text Preprocessor Module")
