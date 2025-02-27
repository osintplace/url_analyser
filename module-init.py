"""
News Analyzer Library

A comprehensive toolkit for analyzing news articles from various sources,
extracting structured information, and generating standardized analysis.

Main components:
- Fetchers: Retrieve content from various sources
- Extractors: Extract specific information from article text
- Analyzers: Orchestrate the analysis process
- Models: Data structures for articles and analysis results
"""

__version__ = "0.1.0"

# Import main functionality for easy access
from news_analyzer.analyzers.bbc_analyzer import BBCAnalyzer
from news_analyzer.models.analysis_result import AnalysisResult
from news_analyzer.fetchers.web_fetcher import WebFetcher
from news_analyzer.fetchers.file_fetcher import FileFetcher

# Convenient functions for end users
def analyze_bbc_from_url(url):
    """Analyze a BBC article from its URL"""
    from news_analyzer.analyzers.bbc_analyzer import BBCAnalyzer
    analyzer = BBCAnalyzer()
    return analyzer.analyze_from_url(url)

def analyze_bbc_from_text(text, url=None):
    """Analyze BBC article text"""
    from news_analyzer.analyzers.bbc_analyzer import BBCAnalyzer
    analyzer = BBCAnalyzer()
    return analyzer.analyze_from_text(text, url)

def analyze_bbc_from_file(filepath, url=None):
    """Analyze a BBC article from a local file"""
    from news_analyzer.analyzers.bbc_analyzer import BBCAnalyzer
    from news_analyzer.fetchers.file_fetcher import FileFetcher
    
    fetcher = FileFetcher()
    content = fetcher.fetch(filepath)
    
    analyzer = BBCAnalyzer()
    return analyzer.analyze_from_text(content, url)
