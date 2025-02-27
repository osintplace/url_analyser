"""
Web fetcher for retrieving article content from URLs.
"""

import requests
from urllib.parse import urlparse
from news_analyzer.fetchers.base_fetcher import BaseFetcher


class WebFetcher(BaseFetcher):
    """
    Fetches content from web URLs.
    
    Handles different HTTP methods, headers, and error conditions.
    """
    
    def __init__(self, timeout=10, headers=None):
        """
        Initialize the web fetcher with custom settings.
        
        Args:
            timeout (int): Request timeout in seconds
            headers (dict, optional): Custom HTTP headers
        """
        self.timeout = timeout
        
        # Default headers that mimic a browser to avoid being blocked
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
    
    def fetch(self, url):
        """
        Fetch content from a URL.
        
        Args:
            url (str): The URL to fetch content from
            
        Returns:
            str: The content of the URL
            
        Raises:
            ValueError: If the URL is invalid
            ConnectionError: If the URL cannot be fetched
        """
        # Validate URL
        if not url:
            raise ValueError("URL cannot be empty")
        
        # Parse URL to ensure it's valid
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError(f"Invalid URL: {url}")
        
        try:
            # Make the HTTP request
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout
            )
            
            # Raise an exception for HTTP errors
            response.raise_for_status()
            
            # Return the content
            return response.text
        
        except requests.exceptions.RequestException as e:
            # Convert requests exceptions to a more generic error
            raise ConnectionError(f"Error fetching URL {url}: {str(e)}")
    
    def fetch_with_metadata(self, url):
        """
        Fetch content along with HTTP metadata.
        
        Args:
            url (str): The URL to fetch
            
        Returns:
            dict: Dictionary with content and metadata
        """
        # Validate URL
        if not url:
            raise ValueError("URL cannot be empty")
        
        try:
            # Make the HTTP request
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout
            )
            
            # Raise an exception for HTTP errors
            response.raise_for_status()
            
            # Return the content and metadata
            return {
                "content": response.text,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "url": response.url,  # Final URL after any redirects
                "encoding": response.encoding,
                "content_type": response.headers.get("Content-Type")
            }
        
        except requests.exceptions.RequestException as e:
            # Convert requests exceptions to a more generic error
            raise ConnectionError(f"Error fetching URL {url}: {str(e)}")
