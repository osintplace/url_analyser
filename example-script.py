#!/usr/bin/env python3
"""
Example script demonstrating how to use the news_analyzer library to analyze news articles from URLs.

Usage:
    python analyze_article.py
"""

import os
import sys
import argparse
import datetime
import pathlib
from pprint import pprint

# =======================================================================
# INPUT SECTION - MODIFY THIS URL TO ANALYZE A DIFFERENT NEWS ARTICLE
# =======================================================================
# Default news article URL to analyze
DEFAULT_URL = "https://www.bbc.co.uk/news/articles/cewkkkvkzn9o"
# Output folder for analysis results
OUTPUT_FOLDER = "output"
# =======================================================================

# Add parent directory to path so we can import the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from news_analyzer import analyze_bbc_from_url as analyze_from_url_function
except ImportError:
    print("Error: Could not import news_analyzer. Make sure it's installed or in the Python path.")
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
    
    args = parser.parse_args()
    
    # Determine output file (None if --no-output is specified)
    output_file = None if args.no_output else args.output
    
    # Run the analysis
    analyze_from_url(args.url, output_file)


# If script is run directly (not imported), execute the main function
if __name__ == "__main__":
    # For quick testing without command line arguments, you can uncomment and modify these lines:
    # url_to_analyze = "https://www.bbc.co.uk/news/world-us-canada-68408646"
    # analyze_from_url(url_to_analyze, generate_output_filename())
    
    # Run with command line argument parsing
    main()
