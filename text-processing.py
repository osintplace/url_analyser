"""
Text processing utilities for working with article text.
"""

import re
import unicodedata


def normalize_text(text):
    """
    Normalize text by removing excess whitespace and normalizing Unicode.
    
    Args:
        text (str): The text to normalize
        
    Returns:
        str: Normalized text
    """
    if not text:
        return ""
    
    # Normalize Unicode characters
    text = unicodedata.normalize('NFKC', text)
    
    # Replace multiple whitespace with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove whitespace at the beginning and end of lines
    text = re.sub(r'^\s+|\s+$', '', text, flags=re.MULTILINE)
    
    return text.strip()


def split_into_sentences(text):
    """
    Split text into sentences using smarter rules than simple splitting.
    
    Handles common abbreviations and edge cases.
    
    Args:
        text (str): The text to split into sentences
        
    Returns:
        list: List of sentences
    """
    # First normalize the text
    text = normalize_text(text)
    
    # Common abbreviations to ignore when splitting
    abbreviations = [
        r'Mr\.', r'Mrs\.', r'Ms\.', r'Dr\.', r'Prof\.', 
        r'Inc\.', r'Ltd\.', r'Co\.', r'Corp\.', 
        r'vs\.', r'e\.g\.', r'i\.e\.', r'etc\.', 
        r'Jan\.', r'Feb\.', r'Mar\.', r'Apr\.', r'Jun\.', r'Jul\.', 
        r'Aug\.', r'Sep\.', r'Oct\.', r'Nov\.', r'Dec\.'
    ]
    
    # Replace abbreviations with a temporary placeholder
    for abbr in abbreviations:
        text = re.sub(abbr, abbr.replace('.', '###'), text)
    
    # Split on sentence boundaries
    # This looks for periods, exclamation points, or question marks
    # followed by whitespace and then an uppercase letter
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    
    # Restore the periods in abbreviations
    sentences = [s.replace('###', '.') for s in sentences]
    
    # Remove any empty sentences
    sentences = [s for s in sentences if s.strip()]
    
    return sentences


def extract_sentences_with_keyword(text, keyword, context_sentences=0):
    """
    Extract sentences containing a keyword, with optional context.
    
    Args:
        text (str): The text to search
        keyword (str): The keyword to search for
        context_sentences (int): Number of sentences to include before and after
        
    Returns:
        list: List of sentence groups containing the keyword
    """
    # Convert keyword to lowercase for case-insensitive matching
    keyword_lower = keyword.lower()
    
    # Split text into sentences
    sentences = split_into_sentences(text)
    
    # Find sentences with the keyword
    results = []
    
    for i, sentence in enumerate(sentences):
        # Check if keyword is in the sentence (case-insensitive)
        if keyword_lower in sentence.lower():
            # Determine the range of sentences to include
            start = max(0, i - context_sentences)
            end = min(len(sentences), i + context_sentences + 1)
            
            # Extract the sentence group
            group = sentences[start:end]
            
            # Join the sentences and add to results
            results.append(' '.join(group))
    
    return results


def calculate_text_complexity(text):
    """
    Calculate the complexity of the text.
    
    Uses metrics like average sentence length, word length,
    and syllable count.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: Text complexity metrics
    """
    # Normalize the text
    text = normalize_text(text)
    
    # Split into sentences
    sentences = split_into_sentences(text)
    
    # Count sentences
    sentence_count = len(sentences)
    
    # Split into words (filtering out empty strings)
    words = [word for word in re.split(r'\W+', text) if word]
    
    # Count words
    word_count = len(words)
    
    # Calculate average sentence length (in words)
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    
    # Calculate average word length (in characters)
    avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
    
    # Simple function to estimate syllables in a word
    def count_syllables(word):
        word = word.lower()
        # Count vowel groups as syllables
        count = len(re.findall(r'[aeiouy]+', word))
        # Adjust for common patterns
        if word.endswith('e') and len(word) > 2 and word[-2] not in 'aeiouy':
            count -= 1
        if count == 0:
            count = 1
        return count
    
    # Calculate total syllables
    total_syllables = sum(count_syllables(word) for word in words)
    
    # Calculate average syllables per word
    avg_syllables_per_word = total_syllables / word_count if word_count > 0 else 0
    
    # Calculate Flesch Reading Ease score
    # Higher scores indicate easier reading
    # Formula: 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
    flesch_reading_ease = (
        206.835 - 
        (1.015 * avg_sentence_length) - 
        (84.6 * avg_syllables_per_word)
    ) if sentence_count > 0 and word_count > 0 else 0
    
    # Return all metrics
    return {
        'sentence_count': sentence_count,
        'word_count': word_count,
        'avg_sentence_length': avg_sentence_length,
        'avg_word_length': avg_word_length,
        'avg_syllables_per_word': avg_syllables_per_word,
        'flesch_reading_ease': flesch_reading_ease,
        'readability_level': get_readability_level(flesch_reading_ease)
    }


def get_readability_level(flesch_score):
    """
    Convert Flesch Reading Ease score to a readability level.
    
    Args:
        flesch_score (float): Flesch Reading Ease score
        
    Returns:
        str: Readability level description
    """
    if flesch_score >= 90:
        return "Very Easy - 5th-grade level"
    elif flesch_score >= 80:
        return "Easy - 6th-grade level"
    elif flesch_score >= 70:
        return "Fairly Easy - 7th-grade level"
    elif flesch_score >= 60:
        return "Standard - 8th & 9th-grade level"
    elif flesch_score >= 50:
        return "Fairly Difficult - 10th to 12th-grade level"
    elif flesch_score >= 30:
        return "Difficult - College level"
    else:
        return "Very Difficult - College graduate level"
