"""
HTML utilities for parsing and extracting content from HTML documents.
"""

from bs4 import BeautifulSoup


def extract_article_from_html(html, source=None):
    """
    Extract article text from HTML content.
    
    Can use source-specific extraction rules for better accuracy.
    
    Args:
        html (str): The HTML content
        source (str, optional): Source identifier (e.g., 'bbc', 'guardian')
        
    Returns:
        str: Extracted article text
    """
    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style", "noscript", "iframe", "svg"]):
        script.decompose()
    
    # Source-specific extraction
    if source and source.lower() == 'bbc':
        return _extract_bbc_article(soup)
    
    # Generic extraction (fallback)
    return _extract_generic_article(soup)


def _extract_bbc_article(soup):
    """
    Extract article text from BBC HTML using BBC's structure.
    
    Args:
        soup (BeautifulSoup): Parsed HTML
        
    Returns:
        str: Extracted article text
    """
    # Get the headline
    headline = soup.find('h1')
    headline_text = headline.get_text().strip() if headline else ""
    
    # Get article content
    article = soup.find('article')
    
    if not article:
        # Fallback to generic extraction
        return _extract_generic_article(soup)
    
    # Extract all paragraphs from the article
    paragraphs = article.find_all('p')
    
    # Join headline and paragraphs into a single text
    article_text = headline_text + "\n\n"
    article_text += "\n\n".join([p.get_text().strip() for p in paragraphs])
    
    # Look for publication information
    publication_info = soup.find(class_='ssrcss-vtbxng-MetadataStripItem')
    if publication_info:
        article_text += "\n\n" + publication_info.get_text().strip()
    
    return article_text


def _extract_generic_article(soup):
    """
    Extract article text using generic approaches.
    
    This method tries various common article structures.
    
    Args:
        soup (BeautifulSoup): Parsed HTML
        
    Returns:
        str: Extracted article text
    """
    content = []
    
    # Get the headline
    headline = soup.find('h1')
    if headline:
        content.append(headline.get_text().strip())
    
    # Try common article container classes and IDs
    article_containers = [
        soup.find('article'),
        soup.find(id='content'),
        soup.find(id='article'),
        soup.find(id='main'),
        soup.find(class_='article'),
        soup.find(class_='content'),
        soup.find(class_='story'),
        soup.find(class_='post')
    ]
    
    # Use the first valid container found
    article = next((container for container in article_containers if container), None)
    
    if article:
        # Extract paragraphs from the article container
        paragraphs = article.find_all('p')
        content.extend([p.get_text().strip() for p in paragraphs])
    else:
        # Fallback: extract all paragraphs from the document
        paragraphs = soup.find_all('p')
        content.extend([p.get_text().strip() for p in paragraphs])
    
    # Join all content with newlines
    return "\n\n".join(content)


def extract_metadata_from_html(html):
    """
    Extract metadata from HTML content.
    
    Looks for meta tags, Open Graph tags, and other common metadata.
    
    Args:
        html (str): The HTML content
        
    Returns:
        dict: Extracted metadata
    """
    soup = BeautifulSoup(html, 'html.parser')
    metadata = {}
    
    # Extract title
    title_tag = soup.find('title')
    if title_tag:
        metadata['title'] = title_tag.get_text().strip()
    
    # Extract meta tags
    for meta in soup.find_all('meta'):
        # Standard meta tags
        if meta.get('name') and meta.get('content'):
            metadata[meta['name']] = meta['content']
        
        # OpenGraph meta tags
        if meta.get('property') and meta.get('content'):
            if meta['property'].startswith('og:'):
                key = meta['property'][3:]  # Remove 'og:' prefix
                metadata[key] = meta['content']
    
    # Extract canonical URL
    canonical = soup.find('link', rel='canonical')
    if canonical and canonical.get('href'):
        metadata['canonical_url'] = canonical['href']
    
    return metadata
