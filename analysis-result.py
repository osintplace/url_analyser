"""
Analysis result model for representing analyzed article data.
"""

import json


class AnalysisResult:
    """
    Model representing the result of article analysis.
    
    Provides methods for accessing and manipulating analysis data,
    as well as serialization to various formats.
    """
    
    def __init__(self, data=None):
        """
        Initialize an analysis result with data.
        
        Args:
            data (dict, optional): Initial analysis data
        """
        self.data = data or {
            "response": {
                "query_datetime": "",
                "source_name": "",
                "source_evaluation": "",
                "source_credibility": "",
                "source_perspective": "",
                "extracted_urls": []
            },
            "publication": {
                "publication_url": "",
                "publication_date": "",
                "publication_summary": "",
                "publication_keypoints": [],
                "publication_sentiment": [],
                "sentiment_analysis": []
            }
        }
    
    def to_dict(self):
        """
        Convert analysis results to a dictionary.
        
        Returns:
            dict: The analysis data as a dictionary
        """
        return self.data
    
    def to_json(self, indent=2):
        """
        Convert analysis results to a JSON string.
        
        Args:
            indent (int): JSON indentation level
            
        Returns:
            str: JSON representation of the analysis
        """
        return json.dumps(self.data, indent=indent)
    
    def save_to_file(self, filepath, format='json'):
        """
        Save analysis results to a file.
        
        Args:
            filepath (str): Path to save the file
            format (str): Output format ('json' or 'txt')
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                if format.lower() == 'json':
                    file.write(self.to_json())
                else:
                    file.write(self.to_text())
            return True
        except Exception:
            return False
    
    def to_text(self):
        """
        Convert analysis results to a human-readable text format.
        
        Returns:
            str: Formatted text representation
        """
        text = []
        
        # Response information
        response = self.data.get("response", {})
        text.append("ARTICLE ANALYSIS")
        text.append("=" * 50)
        text.append(f"Analysis Date: {response.get('query_datetime', 'Not specified')}")
        text.append(f"Source: {response.get('source_name', 'Not specified')}")
        text.append(f"Source Credibility: {response.get('source_credibility', 'Not specified')}")
        text.append("")
        
        # Publication information
        publication = self.data.get("publication", {})
        text.append("PUBLICATION DETAILS")
        text.append("-" * 50)
        text.append(f"URL: {publication.get('publication_url', 'Not specified')}")
        text.append(f"Date: {publication.get('publication_date', 'Not specified')}")
        text.append("")
        
        # Summary
        text.append("SUMMARY")
        text.append("-" * 50)
        text.append(publication.get("publication_summary", "No summary available"))
        text.append("")
        
        # Key points
        text.append("KEY POINTS")
        text.append("-" * 50)
        for i, point in enumerate(publication.get("publication_keypoints", []), 1):
            text.append(f"{i}. {point}")
        if not publication.get("publication_keypoints"):
            text.append("No key points identified")
        text.append("")
        
        # Sentiment
        text.append("SENTIMENT ANALYSIS")
        text.append("-" * 50)
        text.append(f"Overall: {', '.join(publication.get('publication_sentiment', ['Not analyzed']))}")
        text.append("")
        for analysis in publication.get("sentiment_analysis", []):
            text.append(f"- {analysis}")
        if not publication.get("sentiment_analysis"):
            text.append("No detailed sentiment analysis available")
        text.append("")
        
        # URLs
        text.append("EXTRACTED URLS")
        text.append("-" * 50)
        for url in response.get("extracted_urls", []):
            text.append(f"- {url}")
        if not response.get("extracted_urls"):
            text.append("No URLs extracted")
        
        return "\n".join(text)
    
    def __str__(self):
        """
        String representation of the analysis result.
        
        Returns:
            str: String representation
        """
        response = self.data.get("response", {})
        publication = self.data.get("publication", {})
        
        return (
            f"Analysis of {response.get('source_name', 'unknown source')}, "
            f"published on {publication.get('publication_date', 'unknown date')}"
        )
