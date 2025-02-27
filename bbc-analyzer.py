"""
BBC-specific analyzer that understands the structure and conventions of BBC News articles.
"""

import json
import re
from urllib.parse import urlparse

from news_analyzer.analyzers.base_analyzer import BaseAnalyzer
from news_analyzer.extractors.url_extractor import URLExtractor
from news_analyzer.extractors.key_points_extractor import KeyPointsExtractor
from news_analyzer.extractors.sentiment_analyzer import SentimentAnalyzer
from news_analyzer.extractors.publication_info import PublicationInfoExtractor
from news_analyzer.fetchers.web_fetcher import WebFetcher
from news_analyzer.models.analysis_result import AnalysisResult
from news_analyzer.utils.html_utils import extract_article_from_html


class BBCAnalyzer(BaseAnalyzer):
    """
    Analyzer specifically designed for BBC News articles.
    
    This analyzer understands BBC's HTML structure, publication date formats,
    and other BBC-specific conventions.
    """
    
    def __init__(self):
        """Initialize BBC analyzer with required components"""
        super().__init__()
        self.url_extractor = URLExtractor()
        self.key_points_extractor = KeyPointsExtractor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.publication_info_extractor = PublicationInfoExtractor()
        self.web_fetcher = WebFetcher()
    
    def analyze_from_text(self, text, url=None):
        """
        Analyze BBC article text and return structured results.
        
        Args:
            text (str): The full article text
            url (str, optional): The source URL
            
        Returns:
            AnalysisResult: Structured analysis results
        """
        if url:
            self._validate_source(url)
        
        # Extract URLs from the article
        urls = self.url_extractor.extract(text)
        
        # Extract key points from the article
        key_points = self.key_points_extractor.extract(text, count=5)
        
        # Analyze sentiment
        sentiment_labels, sentiment_analysis = self.sentiment_analyzer.analyze(text)
        
        # Extract publication information
        publication_info = self.publication_info_extractor.extract(text, url)
        
        # Create analysis result structure
        result = {
            "response": {
                "query_datetime": self.analysis_date,
                "source_name": "BBC News",
                "source_evaluation": "Established news organization with strong journalistic standards",
                "source_credibility": "High - BBC is a reputable public service broadcaster with extensive fact-checking processes",
                "source_perspective": "Factual reporting with balanced perspectives",
                "extracted_urls": urls
            },
            "publication": {
                "publication_url": publication_info.get("url", url or "URL not provided"),
                "publication_date": publication_info.get("date", "Date not found"),
                "publication_summary": publication_info.get("summary", "Summary not available"),
                "publication_keypoints": key_points,
                "publication_sentiment": sentiment_labels,
                "sentiment_analysis": sentiment_analysis
            }
        }
        
        return AnalysisResult(result)
    
    def analyze_from_url(self, url):
        """
        Fetch and analyze a BBC article from its URL.
        
        Args:
            url (str): The URL of the BBC article
            
        Returns:
            AnalysisResult: Structured analysis results
            
        Raises:
            ValueError: If the URL is not from BBC
            ConnectionError: If the article cannot be fetched
        """
        if not self._validate_source(url):
            raise ValueError(f"URL is not from BBC News: {url}")
        
        # Fetch the article HTML
        html_content = self.web_fetcher.fetch(url)
        
        # Extract the article text from HTML
        article_text = extract_article_from_html(html_content, source="bbc")
        
        # Analyze the extracted text
        return self.analyze_from_text(article_text, url)
    
    def _validate_source(self, url):
        """
        Check if the URL is from BBC News.
        
        Args:
            url (str): The URL to check
            
        Returns:
            bool: True if the URL is from BBC, False otherwise
        """
        if not url:
            return False
            
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        return "bbc.co.uk" in domain or "bbc.com" in domain
    
    def to_json(self, analysis_result):
        """
        Convert analysis result to JSON string.
        
        Args:
            analysis_result (AnalysisResult): Analysis result to convert
            
        Returns:
            str: JSON string representation
        """
        return json.dumps(analysis_result.to_dict(), indent=2)
