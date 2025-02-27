#!/usr/bin/env python3
"""
Example script demonstrating how to use the news_analyzer library to analyze BBC articles.

This script shows two approaches:
1. Analyzing an article from a URL
2. Analyzing an article from a local file

Usage:
    python analyze_bbc_article.py
"""

import os
import sys
import argparse
from pprint import pprint

# Add parent directory to path so we can import the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from news_analyzer import analyze_bbc_from_url, analyze_bbc_from_file
except ImportError:
    print("Error: Could not import news_analyzer. Make sure it's installed or in the Python path.")
    sys.exit(1)


def analyze_from_url(url, output_file=None):
    """
    Analyze a BBC article from a URL.
    
    Args:
        url (str): The URL of the BBC article
        output_file (str, optional): Path to save results
    """
    print(f"Analyzing BBC article from URL: {url}")
    
    try:
        # Perform the analysis
        result = analyze_bbc_from_url(url)
        
        # Print summary to console
        print("\nAnalysis Results:")
        print("-" * 50)
        print(f"Source: {result.data['response']['source_name']}")
        print(f"Date: {result.data['publication']['publication_date']}")
        print(f"Sentiment: {', '.join(result.data['publication']['publication_sentiment'])}")
        print("\nKey Points:")
        for i, point in enumerate(result.data['publication']['publication_keypoints'], 1):
            print(f"{i}. {point}")
        
        # Save results if requested
        if output_file:
            if result.save_to_file(output_file):
                print(f"\nFull analysis saved to: {output_file}")
            else:
                print(f"\nError: Could not save analysis to {output_file}")
        
        return result
        
    except Exception as e:
        print(f"Error analyzing article: {str(e)}")
        return None


def analyze_from_file(filepath, url=None, output_file=None):
    """
    Analyze a BBC article from a local text file.
    
    Args:
        filepath (str): Path to the file containing article text
        url (str, optional): URL of the article
        output_file (str, optional): Path to save results
    """
    print(f"Analyzing BBC article from file: {filepath}")
    
    try:
        # Perform the analysis
        result = analyze_bbc_from_file(filepath, url)
        
        # Print summary to console
        print("\nAnalysis Results:")
        print("-" * 50)
        print(f"Source: {result.data['response']['source_name']}")
        
        # Only print date if it was successfully extracted
        if result.data['publication']['publication_date']:
            print(f"Date: {result.data['publication']['publication_date']}")
        
        print(f"Sentiment: {', '.join(result.data['publication']['publication_sentiment'])}")
        print("\nKey Points:")
        for i, point in enumerate(result.data['publication']['publication_keypoints'], 1):
            print(f"{i}. {point}")
        
        # Save results if requested
        if output_file:
            if result.save_to_file(output_file):
                print(f"\nFull analysis saved to: {output_file}")
            else:
                print(f"\nError: Could not save analysis to {output_file}")
        
        return result
        
    except Exception as e:
        print(f"Error analyzing article: {str(e)}")
        return None


def main():
    """Main function that parses arguments and calls appropriate functions."""
    
    parser = argparse.ArgumentParser(description="Analyze BBC News articles.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--url", help="URL of BBC article to analyze")
    group.add_argument("-f", "--file", help="File containing BBC article text")
    parser.add_argument("-o", "--output", help="Output file for analysis results")
    
    args = parser.parse_args()
    
    if args.url:
        analyze_from_url(args.url, args.output)
    elif args.file:
        # If a file is specified, also allow an optional URL
        url_input = input("Optional: Enter the article URL for reference: ").strip()
        url = url_input if url_input else None
        analyze_from_file(args.file, url, args.output)


if __name__ == "__main__":
    main()
