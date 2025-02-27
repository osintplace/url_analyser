"""
Tests for the URL Extractor component.
"""

import unittest
from news_analyzer.extractors.url_extractor import URLExtractor


class TestURLExtractor(unittest.TestCase):
    """Test cases for the URLExtractor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.extractor = URLExtractor()
        
        # Sample text with URLs
        self.sample_text = """
        This is a test article from BBC News: https://www.bbc.co.uk/news/articles/123456.
        
        The article references another site: https://www.example.com/page1
        and then references it again with a different path: https://www.example.com/page2
        
        It also links to Twitter: https://twitter.com/BBCNews and 
        Instagram: https://www.instagram.com/bbcnews/
        
        Some URLs might have query parameters: https://www.google.com/search?q=news
        
        And some might be mentioned multiple times:
        https://www.bbc.co.uk/news again and https://www.bbc.co.uk/news/articles/789012
        """
    
    def test_extract_unique_urls(self):
        """Test that URLs are correctly extracted and deduplicated."""
        urls = self.extractor.extract(self.sample_text)
        
        # Check that the right number of unique domains were extracted
        self.assertEqual(len(urls), 4)
        
        # Check that all expected domains are present
        expected_domains = [
            "https://www.bbc.co.uk",
            "https://www.example.com",
            "https://twitter.com",
            "https://www.instagram.com"
        ]
        
        # The order should be preserved based on first appearance
        self.assertEqual(urls, expected_domains)
    
    def test_empty_text(self):
        """Test that empty text returns an empty list."""
        urls = self.extractor.extract("")
        self.assertEqual(urls, [])
    
    def test_no_urls(self):
        """Test that text without URLs returns an empty list."""
        text = "This is a text with no URLs in it."
        urls = self.extractor.extract(text)
        self.assertEqual(urls, [])
    
    def test_malformed_urls(self):
        """Test handling of malformed URLs."""
        text = """
        This URL is malformed: www.example.com (no http/https)
        This one too: http:/malformed.com (missing slash)
        """
        urls = self.extractor.extract(text)
        self.assertEqual(urls, [])
    
    def test_extract_with_context(self):
        """Test extraction of URLs with surrounding context."""
        text = "Check out https://example.com for more information."
        results = self.extractor.extract_with_context(text, context_chars=10)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['url'], "https://example.com")
        self.assertTrue("Check out" in results[0]['context'])
        self.assertTrue("for more" in results[0]['context'])


if __name__ == '__main__':
    unittest.main()
