def detect_language(text):
    """
    Detect the language of the given text.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        tuple: (language_code, language_name, is_english)
    """
    try:
        # Detect language using langid
        lang_code, confidence = langid.classify(text)
        
        # Map of language codes to names for common languages
        language_names = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'nl': 'Dutch',
            'ru': 'Russian',
            'uk': 'Ukrainian',
            'be': 'Belarusian',
            'ar': 'Arabic',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ko': 'Korean',
            'hi': 'Hindi',
            'tr': 'Turkish',
            'pl': 'Polish',
            'sv': 'Swedish',
            'da': 'Danish',
            'fi': 'Finnish',
            'no': 'Norwegian',
            'cs': 'Czech'
        }
        
        # Special handling for Russian/Ukrainian detection
        # langid might not distinguish Ukrainian well, so we use additional checks
        if lang_code == 'ru':
            # Ukrainian-specific characters: і, є, ї, ґ
            ukrainian_chars = {'і', 'є', 'ї', 'ґ', 'І', 'Є', 'Ї', 'Ґ'}
            if any(char in text for char in ukrainian_chars):
                lang_code = 'uk'
        
        # Get language name, default to the code if not in our map
        language_name = language_names.get(lang_code, f"Unknown ({lang_code})")
        
        # Check if the language is English
        is_english = (lang_code == 'en')
        
        return lang_code, language_name, is_english
    
    except Exception as e:
        print(f"Warning: Language detection error: {e}")
        return 'en', 'English (assumed)', True


def translate_to_english(text, source_lang=None):
    """
    Translate the given text to English.
    
    Args:
        text (str): The text to translate
        source_lang (str, optional): Source language code
        
    Returns:
        str: Translated text (or original if translation fails)
    """
    if not text or not ENABLE_TRANSLATION:
        return text
    
    # Handle empty or very short text
    if len(text.strip()) < 5:
        return text
        
    try:
        # Initialize translator
        translator = Translator()
        
        # Special handling for Cyrillic (Russian/Ukrainian) text
        if source_lang in ['ru', 'uk', 'be']:
            # Check if Cyrillic characters are present
            if any(ord('а') <= ord(c) <= ord('я') or ord('А') <= ord(c) <= ord('Я') for c in text):
                print(f"Translating Cyrillic text ({source_lang}) with enhanced detection...")
                # Force source language to ensure proper translation
                result = translator.translate(text, dest='en', src=source_lang)
                return result.text
        
        # For other languages, try automatic detection
        result = translator.translate(text, dest='en', src=source_lang)
        return result.text
    except Exception as e:
        print(f"Warning: Translation error: {e}")
        # Try alternative translation approach
        try:
            import requests
            import json
            
            # Simple fallback using a free translation API
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                "client": "gtx",
                "sl": source_lang or "auto",
                "tl": "en",
                "dt": "t",
                "q": text
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                # Extract translated text from response
                result = response.json()
                translated_text = ''.join([part[0] for part in result[0] if part[0]])
                return translated_text
        except Exception as fallback_error:
            print(f"Warning: Fallback translation also failed: {fallback_error}")
        
        return text  # Return original text if all translation attempts fail


def translate_analysis_results(result, source_lang):
    """
    Translate the key parts of the analysis results to English.
    
    Args:
        result (dict): The analysis result data
        source_lang (str): Source language code
        
    Returns:
        dict: The analysis result with translated fields
    """
    if not ENABLE_TRANSLATION or source_lang == 'en':
        return result
    
    # Make a deep copy to avoid modifying the original
    import copy
    translated_result = copy.deepcopy(result)
    
    # Translate publication summary
    if 'publication' in translated_result and 'publication_summary' in translated_result['publication']:
        summary = translated_result['publication']['publication_summary']
        translated_result['publication']['publication_summary'] = translate_to_english(summary, source_lang)
        
        # Store the original summary
        translated_result['publication']['original_summary'] = summary
    
    # Translate key points
    if 'publication' in translated_result and 'publication_keypoints' in translated_result['publication']:
        key_points = translated_result['publication']['publication_keypoints']
        translated_key_points = [translate_to_english(point, source_lang) for point in key_points]
        
        # Store the original key points
        translated_result['publication']['original_keypoints'] = key_points
        
        # Update with translated key points
        translated_result['publication']['publication_keypoints'] = translated_key_points
    
    # Translate sentiment analysis
    if 'publication' in translated_result and 'sentiment_analysis' in translated_result['publication']:
        sentiment_analysis = translated_result['publication']['sentiment_analysis']
        translated_sentiment = [translate_to_english(text, source_lang) for text in sentiment_analysis]
        
        # Store the original sentiment analysis
        translated_result['publication']['original_sentiment_analysis'] = sentiment_analysis
        
        # Update with translated sentiment analysis
        translated_result['publication']['sentiment_analysis'] = translated_sentiment
    
    # Add translation metadata
    translated_result['translation'] = {
        'performed': True,
        'source_language': source_lang,
        'target_language': 'en'
    }
    
    return translated_result#!/usr/bin/env python3
"""
Example script demonstrating how to use the news_analyzer library to analyze news articles from URLs.
Includes automatic language detection and translation for non-English content.

Usage:
    python analyze_article.py
"""

import os
import sys
import argparse
import datetime
import pathlib
import requests
from pprint import pprint

# =======================================================================
# INPUT SECTION - MODIFY THIS URL TO ANALYZE A DIFFERENT NEWS ARTICLE
# =======================================================================
# Default news article URL to analyze
DEFAULT_URL = "https://www.bbc.co.uk/news/articles/cewkkkvkzn9o"
# Output folder for analysis results
OUTPUT_FOLDER = "output"
# Enable automatic translation (set to False to disable)
ENABLE_TRANSLATION = True
# =======================================================================

# Add parent directory to path so we can import the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from news_analyzer import analyze_bbc_from_url as analyze_from_url_function
    # Import translation-related packages
    import langid
    from googletrans import Translator
except ImportError as e:
    print(f"Error: {e}")
    print("\nMake sure all required packages are installed:")
    print("pip install news_analyzer langid googletrans==4.0.0-rc1")
    sys.exit(1)


def ensure_output_folder_exists():
    """
    Create the output folder if it doesn't exist.
    
    Returns:
        str: Path to the output folder
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create complete path to output folder
    output_folder = os.path.join(script_dir, OUTPUT_FOLDER)
    
    # Create the folder if it doesn't exist
    pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    return output_folder


def generate_output_filename():
    """
    Generate an output filename based on the script name with a unique number.
    
    Returns:
        str: Generated filename
    """
    # Get the script name without extension
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    
    # Get the output folder
    output_folder = ensure_output_folder_exists()
    
    # Find existing files with the same pattern
    existing_files = [f for f in os.listdir(output_folder) 
                      if f.startswith(script_name) and f.endswith('.json')]
    
    # Find the next number to use
    next_num = 1
    if existing_files:
        # Extract numbers from existing filenames
        nums = []
        for filename in existing_files:
            # Extract the numeric part between the script name and .json
            num_part = filename[len(script_name):-5]
            if num_part.startswith('-') and num_part[1:].isdigit():
                nums.append(int(num_part[1:]))
        
        if nums:
            next_num = max(nums) + 1
    
    # Format with leading zeros to ensure proper sorting
    return f"{script_name}-{next_num:03d}.json"


def analyze_from_url(url, output_file=None):
    """
    Analyze a news article from a URL.
    
    Args:
        url (str): The URL of the news article
        output_file (str, optional): Path to save results
        
    Returns:
        AnalysisResult: The analysis result object or None if an error occurred
    """
    print(f"Analyzing news article from URL: {url}")
    
    try:
        # Perform the analysis
        result = analyze_from_url_function(url)
        
        # Detect language in the article summary
        summary = result.data['publication']['publication_summary']
        lang_code, lang_name, is_english = detect_language(summary)
        
        print(f"\nDetected language: {lang_name} ({lang_code})")
        
        # Special message for Russian or Ukrainian content
        if lang_code in ['ru', 'uk']:
            print(f"Detected {lang_name} content, applying specialized translation...")
        
        # Translate if not in English
        if not is_english and ENABLE_TRANSLATION:
            print(f"Translating content from {lang_name} to English...")
            result.data = translate_analysis_results(result.data, lang_code)
            print("Translation complete.")
        
        # Print summary to console
        print("\nAnalysis Results:")
        print("-" * 50)
        print(f"Source: {result.data['response']['source_name']}")
        print(f"Date: {result.data['publication']['publication_date']}")
        print(f"Sentiment: {', '.join(result.data['publication']['publication_sentiment'])}")
        
        # Print extracted URLs
        print("\nExtracted URLs:")
        for url in result.data['response']['extracted_urls']:
            print(f"- {url}")
        
        print("\nKey Points:")
        for i, point in enumerate(result.data['publication']['publication_keypoints'], 1):
            print(f"{i}. {point}")
        
        # Display original language information if translated
        if not is_english and ENABLE_TRANSLATION and 'translation' in result.data:
            print(f"\nOriginal content was in {lang_name} and has been translated to English.")
            print("Original content is preserved in the JSON output.")
        
        # Save results if requested
        if output_file:
            # Ensure output folder exists
            output_folder = ensure_output_folder_exists()
            
            # Create full path to output file
            full_output_path = os.path.join(output_folder, output_file)
            
            if result.save_to_file(full_output_path):
                print(f"\nFull analysis saved to: {full_output_path}")
            else:
                print(f"\nError: Could not save analysis to {full_output_path}")
        
        return result
        
    except Exception as e:
        print(f"Error analyzing article: {str(e)}")
        return None


def main():
    """Main function that parses arguments and calls the analyzer."""
    
    # Generate output filename based on script name
    default_output_file = generate_output_filename()
    
    parser = argparse.ArgumentParser(description="Analyze news articles from URLs.")
    parser.add_argument("-u", "--url", 
                      help=f"URL of news article to analyze (default: {DEFAULT_URL})",
                      default=DEFAULT_URL)
    parser.add_argument("-o", "--output", 
                      help=f"Output filename (default: {default_output_file})",
                      default=default_output_file)
    parser.add_argument("--no-output", 
                      help="Skip saving results to a file",
                      action="store_true")
    parser.add_argument("--no-translation",
                      help="Disable automatic translation of non-English content",
                      action="store_true")
    
    args = parser.parse_args()
    
    # Determine output file (None if --no-output is specified)
    output_file = None if args.no_output else args.output
    
    # Set translation setting
    global ENABLE_TRANSLATION
    if args.no_translation:
        ENABLE_TRANSLATION = False
    
    # Run the analysis
    analyze_from_url(args.url, output_file)


# If script is run directly (not imported), execute the main function
if __name__ == "__main__":
    # Check for required packages
    try:
        import langid
        from googletrans import Translator
        print("Language detection and translation packages found.")
    except ImportError:
        print("Warning: Some required packages for translation are missing.")
        print("To enable translation features, install: pip install langid googletrans==4.0.0-rc1")
        ENABLE_TRANSLATION = False
    
    # For quick testing without command line arguments, you can uncomment and modify these lines:
    # url_to_analyze = "https://www.pravda.com.ua/news/" # Ukrainian news site
    # analyze_from_url(url_to_analyze, generate_output_filename())
    
    # Run with command line argument parsing
    main()
