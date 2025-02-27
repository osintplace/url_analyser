"""
JSON formatting utilities for standardizing analysis output.
"""

import json
import datetime


class JSONFormatter:
    """
    Formats analysis data into standardized JSON structures.
    
    Handles data validation, transformation, and formatting
    to ensure consistent output across different analyzers.
    """
    
    def __init__(self, indent=2, ensure_ascii=False):
        """
        Initialize the formatter with custom settings.
        
        Args:
            indent (int): JSON indentation level
            ensure_ascii (bool): Whether to escape non-ASCII characters
        """
        self.indent = indent
        self.ensure_ascii = ensure_ascii
    
    def format_analysis(self, data):
        """
        Format analysis data into the standard structure.
        
        Ensures all required fields are present, even if empty.
        
        Args:
            data (dict): The analysis data to format
            
        Returns:
            dict: Formatted data with all required fields
        """
        # Ensure response section exists
        if 'response' not in data:
            data['response'] = {}
        
        # Ensure publication section exists
        if 'publication' not in data:
            data['publication'] = {}
        
        # Ensure all required fields exist in response section
        response_fields = [
            'query_datetime', 'source_name', 'source_evaluation',
            'source_credibility', 'source_perspective', 'extracted_urls'
        ]
        
        for field in response_fields:
            if field not in data['response']:
                data['response'][field] = [] if field == 'extracted_urls' else ""
        
        # Ensure all required fields exist in publication section
        publication_fields = [
            'publication_url', 'publication_date', 'publication_summary',
            'publication_keypoints', 'publication_sentiment', 'sentiment_analysis'
        ]
        
        for field in publication_fields:
            if field not in data['publication']:
                data['publication'][field] = (
                    [] if field in ['publication_keypoints', 'publication_sentiment', 'sentiment_analysis']
                    else ""
                )
        
        # Ensure date fields are standardized
        if not data['response']['query_datetime']:
            data['response']['query_datetime'] = datetime.datetime.now().strftime("%B %d, %Y")
        
        return data
    
    def to_json(self, data):
        """
        Convert data to a JSON string with proper formatting.
        
        Args:
            data (dict): The data to convert to JSON
            
        Returns:
            str: Formatted JSON string
        """
        # First, ensure the data is properly formatted
        formatted_data = self.format_analysis(data)
        
        # Convert to JSON string
        return json.dumps(
            formatted_data,
            indent=self.indent,
            ensure_ascii=self.ensure_ascii
        )
    
    def to_pretty_json(self, data):
        """
        Convert data to a nicely formatted JSON string for display.
        
        Args:
            data (dict): The data to convert to JSON
            
        Returns:
            str: Formatted JSON string with colors (if supported in terminal)
        """
        try:
            # Try to import pygments for syntax highlighting
            from pygments import highlight
            from pygments.lexers import JsonLexer
            from pygments.formatters import TerminalFormatter
            
            # Format the data
            json_str = self.to_json(data)
            
            # Apply syntax highlighting
            return highlight(json_str, JsonLexer(), TerminalFormatter())
        
        except ImportError:
            # Fall back to normal JSON if pygments is not available
            return self.to_json(data)
    
    def save_to_file(self, data, filepath):
        """
        Save data to a JSON file.
        
        Args:
            data (dict): The data to save
            filepath (str): Path to save the file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Format the data
            formatted_data = self.format_analysis(data)
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(
                    formatted_data,
                    file,
                    indent=self.indent,
                    ensure_ascii=self.ensure_ascii
                )
            return True
        
        except Exception:
            return False
