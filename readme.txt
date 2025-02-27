# News Analyzer

A comprehensive Python library for analyzing news articles from various sources, extracting structured information, and generating standardized analysis in JSON format.

## Features

- Extract and deduplicate URLs from article text
- Identify key points through intelligent sentence analysis
- Perform sentiment analysis to determine article tone
- Extract publication metadata (dates, authors, etc.)
- Support for multiple news sources (currently BBC News)
- Output results in JSON or human-readable text formats

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/news_analyzer.git
cd news_analyzer

# Install the package
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Quick Start

```python
from news_analyzer import analyze_bbc_from_url

# Analyze an article from URL
result = analyze_bbc_from_url("https://www.bbc.co.uk/news/articles/cewkkkvkzn9o")

# Print the analysis as JSON
print(result.to_json())

# Save the analysis to a file
result.save_to_file("analysis_result.json")
```

## Command Line Example

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
    "publication_url": "https://www.bbc.co.uk/news/articles/cewkkkvkzn9o",
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