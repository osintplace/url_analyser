"""
Base analyzer module that defines the abstract interface for all analyzers.
"""

from abc import ABC, abstractmethod
from datetime import datetime

class BaseAnalyzer(ABC):
    """
    Abstract base class for article analyzers.
    
    All specific news source analyzers should inherit from this class
    and implement the abstract methods.
    """
    
    def __init__(self):
        """Initialize the analyzer with the current date"""
        self.analysis_date = datetime.now().strftime("%B %d, %Y")
    
    @abstractmethod
    def analyze_from_text(self, text, url=None):
        """
        Analyze article text and return structured analysis results.
        
        Args:
            text (str): The full article text
            url (str, optional): The source URL of the article
            
        Returns:
            AnalysisResult: Structured analysis result
        """
        pass
    
    @abstractmethod
    def analyze_from_url(self, url):
        """
        Fetch and analyze an article from a URL.
        
        Args:
            url (str): The URL of the article to analyze
            
        Returns:
            AnalysisResult: Structured analysis result
        """
        pass
    
    def _validate_source(self, url):
        """
        Validate that the URL is from a source supported by this analyzer.
        
        Args:
            url (str): The URL to validate
            
        Returns:
            bool: True if the URL is from a supported source, False otherwise
        """
        return True  # Default implementation accepts all URLs
