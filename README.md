# News Analyzer

A comprehensive Python library for analyzing news articles from various sources, extracting structured information, and generating standardized analysis in JSON format.

## Features

- Extract and deduplicate URLs from article text
- Identify key points through intelligent sentence analysis
- Perform sentiment analysis to determine article tone
- Extract publication metadata (dates, authors, etc.)
- Support for multiple news sources (currently BBC News)
- Output results in JSON or human-readable text formats

## Project Structure

This project follows a standard Python package structure:

```
news_analyzer/
│
├── __init__.py                 # Package exports
├── analyzers/                  # Article analyzers
│   ├── __init__.py             # Package initialization
│   ├── base_analyzer.py        # Abstract base class
│   └── bbc_analyzer.py         # BBC-specific analyzer
│
├── extractors/                 # Information extractors
│   ├── __init__.py             # Package initialization
│   ├── url_extractor.py        # URL extraction
│   ├── key_points_extractor.py # Key points extraction
│   ├── sentiment_analyzer.py   # Sentiment analysis
│   └── publication_info.py     # Publication metadata
│
├── fetchers/                   # Content fetchers
│   ├── __init__.py             # Package initialization
│   ├── base_fetcher.py         # Abstract base class
│   ├── web_fetcher.py          # HTTP fetching
│   └── file_fetcher.py         # Local file reading
│
├── models/                     # Data models
│   ├── __init__.py             # Package initialization
│   └── analysis_result.py      # Analysis result model
│
├── utils/                      # Utility functions
│   ├── __init__.py             # Package initialization
│   ├── html_utils.py           # HTML parsing utilities
│   ├── text_processing.py      # Text processing utilities
│   └── json_formatter.py       # JSON formatting utilities
│
└── examples/                   # Example scripts
    ├── __init__.py             # Package initialization
    └── analyze_bbc_article.py  # BBC article analyzer
```

## Installation

### Setting up the project

```bash
# Clone the repository
git clone https://github.com/yourusername/news_analyzer.git
cd news_analyzer

# Install the package in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

### Verifying the installation

To verify that the package is installed correctly, you can run a simple test:

```python
from news_analyzer.extractors.url_extractor import URLExtractor

# Create an instance
extractor = URLExtractor()

# Test the extractor
urls = extractor.extract("Test with https://example.com")
print(f"Extracted URLs: {urls}")
```

## Usage Examples

### Analyzing an article from a URL

```python
from news_analyzer import analyze_bbc_from_url

# Analyze an article from URL
result = analyze_bbc_from_url("https://www.bbc.co.uk/news/articles/cewkkkvkzn9o")

# Print the analysis as JSON
print(result.to_json())

# Save the analysis to a file
result.save_to_file("analysis_result.json")
```

### Analyzing an article from a text file

```python
from news_analyzer import analyze_bbc_from_file

# Analyze an article from a file
result = analyze_bbc_from_file("article.txt")

# Print summary information
print(f"Source: {result.data['response']['source_name']}")
print(f"Date: {result.data['publication']['publication_date']}")
print(f"Sentiment: {', '.join(result.data['publication']['publication_sentiment'])}")

# Print key points
print("\nKey Points:")
for i, point in enumerate(result.data['publication']['publication_keypoints'], 1):
    print(f"{i}. {point}")
```

## Command Line Examples

The package includes example scripts that can be run from the command line:

```bash
# Analyze article from a URL
python -m news_analyzer.examples.analyze_bbc_article --url "https://www.bbc.co.uk/news/articles/cewkkkvkzn9o" --output analysis.json

# Analyze article from a text file
python -m news_analyzer.examples.analyze_bbc_article --file article.txt --output analysis.json
```

## Output Format

The analysis is returned in a standardized JSON format:

```json
{
  "response": {
    "query_datetime": "February 27, 2025",
    "source_name": "BBC News",
    "source_evaluation": "Established news organization with strong journalistic standards",
    "source_credibility": "High - BBC is a reputable public service broadcaster with extensive fact-checking processes",
    "source_perspective": "Factual reporting with balanced perspectives",
    "extracted_urls": ["https://example.com", "https://anothersite.org"]
  },
  "publication": {
    "publication_date": "27 February 2025, 08:37 GMT (Updated 1 hour ago)",
    "publication_summary": "Oscar-winning actor Gene Hackman, his wife and their dog were found dead in different rooms of their home in Santa Fe, New Mexico.",
    "publication_keypoints": [
      "Gene Hackman (95) and wife Betsy Arakawa (63) were found deceased at their Santa Fe home",
      "Police reports indicate they had been dead for some time with no signs of wounds",
      "Hackman won two Academy Awards during his distinguished career",
      "He stepped back from Hollywood in 2004 for a quieter life in New Mexico",
      "Tributes from film industry figures highlight his talent and contributions"
    ],
    "publication_sentiment": ["Respectful", "Factual", "Commemorative"],
    "sentiment_analysis": [
      "The article maintains a neutral, factual tone when reporting the circumstances of the deaths",
      "When discussing Hackman's career, the tone becomes celebratory and respectful of his legacy",
      "Industry tributes included in the article express admiration for his talent and contributions to cinema"
    ]
  }
}
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'news_analyzer'**

   Make sure:
   - Your directory structure is correct with all necessary `__init__.py` files
   - You've installed the package with `pip install -e .`
   - You're using the correct Python environment
   
2. **ImportError for specific modules**

   Check that:
   - The file exists in the correct location
   - The filename uses underscores, not hyphens (e.g., `url_extractor.py`, not `url-extractor.py`)
   - The class or function name in the import statement matches the actual name in the file

3. **setup.py not found**

   Ensure that:
   - `setup.py` is in the root directory of your project
   - You're running the pip install command from the directory containing `setup.py`

## Extending the Library

### Adding Support for New News Sources

1. Create a new analyzer class that inherits from `BaseAnalyzer`
2. Implement the required methods for the new source
3. Add any source-specific extraction logic

Example:

```python
from news_analyzer.analyzers.base_analyzer import BaseAnalyzer

class GuardianAnalyzer(BaseAnalyzer):
    """Analyzer for The Guardian articles."""
    
    def __init__(self):
        super().__init__()
        # Initialize extractors
        
    def analyze_from_text(self, text, url=None):
        # Implement Guardian-specific analysis
        
    def analyze_from_url(self, url):
        # Implement Guardian-specific fetching and analysis
        
    def _validate_source(self, url):
        # Check if URL is from The Guardian
        return "theguardian.com" in url
```

## Development

### Running Tests

```bash
pytest
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
