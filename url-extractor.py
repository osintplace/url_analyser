"""
URL extractor module for finding and deduplicating URLs in article text.
"""

import re
from urllib.parse import urlparse


class URLExtractor:
    """
    Extracts URLs from text and provides deduplication functionality.
    """
    
    def __init__(self):
        """Initialize the URL extractor with default regex patterns"""
        # Pattern to match http and https URLs
        self.url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    
    def extract(self, text):
        """
        Extract all URLs from text and remove duplicates.
        
        This method finds all URLs using regex, then deduplicates them
        based on domain to avoid repetitive references to the same site.
        
        Args:
            text (str): The text to extract URLs from
            
        Returns:
            list: A list of unique base URLs
        """
        # Find all URLs in the text using the regex pattern
        urls = re.findall(self.url_pattern, text)
        
        # Remove duplicates while preserving order
        unique_urls = []
        seen_domains = set()
        
        for url in urls:
            # Get base URL without parameters
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            # Only add the URL if we haven't seen this domain before
            if base_url not in seen_domains:
                unique_urls.append(base_url)
                seen_domains.add(base_url)
                
        return unique_urls
    
    def extract_with_context(self, text, context_chars=50):
        """
        Extract URLs with surrounding context.
        
        This is useful for understanding what the URL refers to in the article.
        
        Args:
            text (str): The text to extract URLs from
            context_chars (int): Number of characters of context to include
            
        Returns:
            list: A list of dicts with 'url' and 'context' keys
        """
        urls_with_context = []
        
        for match in re.finditer(self.url_pattern, text):
            url = match.group(0)
            
            # Get start and end positions for context
            start = max(0, match.start() - context_chars)
            end = min(len(text), match.end() + context_chars)
            
            # Extract context
            context = text[start:end]
            
            # Add to results
            urls_with_context.append({
                'url': url,
                'context': context
            })
            
        return urls_with_context
