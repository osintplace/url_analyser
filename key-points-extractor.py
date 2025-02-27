"""
Key points extractor for identifying the most important information in articles.
"""

import re


class KeyPointsExtractor:
    """
    Extracts key points from article text by identifying important sentences.
    
    Uses a combination of keyword matching and sentence structure analysis
    to determine which sentences are most likely to contain key information.
    """
    
    def __init__(self):
        """Initialize with default important keywords for news articles"""
        # Keywords that often indicate important information in news articles
        self.important_keywords = [
            'announced', 'discovered', 'revealed', 'confirmed', 'found',
            'reported', 'launched', 'published', 'released', 'unveiled',
            'decision', 'voted', 'agreement', 'investigation', 'study',
            'research', 'evidence', 'according to', 'statement', 'explained',
            'warned', 'critical', 'significant', 'major', 'crucial',
            'important', 'essential', 'key', 'central', 'vital',
            # Adding person-specific keywords for obituaries/profiles
            'born', 'died', 'award', 'Oscar', 'prize', 'medal', 'honored',
            'career', 'achievement', 'legacy', 'contribution', 'impact'
        ]
        
        # Minimum sentence length to be considered as a key point
        self.min_sentence_length = 30
        
        # Maximum sentence length (very long sentences are often less useful as key points)
        self.max_sentence_length = 200
    
    def extract(self, text, count=5):
        """
        Extract key points from the article text.
        
        Args:
            text (str): The article text
            count (int): Number of key points to extract
            
        Returns:
            list: List of sentences representing key points
        """
        # Split text into sentences
        sentences = self._split_into_sentences(text)
        
        # Score each sentence
        scored_sentences = self._score_sentences(sentences)
        
        # Select top sentences based on score
        top_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)[:count]
        
        # Extract just the sentences from the (sentence, score) tuples
        key_points = [sentence for sentence, score in top_sentences]
        
        # Format sentences for readability
        key_points = [self._format_sentence(sentence) for sentence in key_points]
        
        return key_points
    
    def _split_into_sentences(self, text):
        """
        Split text into individual sentences.
        
        Args:
            text (str): The text to split
            
        Returns:
            list: List of sentences
        """
        # Regex pattern to split on sentence boundaries
        # Looks for periods, exclamation points, or question marks followed by whitespace
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Filter out empty or very short sentences, and trim whitespace
        sentences = [s.strip() for s in sentences if len(s.strip()) > self.min_sentence_length]
        
        return sentences
    
    def _score_sentences(self, sentences):
        """
        Score sentences based on importance indicators.
        
        Args:
            sentences (list): List of sentences to score
            
        Returns:
            list: List of (sentence, score) tuples
        """
        scored_sentences = []
        
        for sentence in sentences:
            # Skip sentences that are too long or too short
            if len(sentence) < self.min_sentence_length or len(sentence) > self.max_sentence_length:
                continue
                
            # Start with base score
            score = 0
            
            # Boost score for sentences with important keywords
            for keyword in self.important_keywords:
                if keyword.lower() in sentence.lower():
                    score += 1
            
            # Boost score for sentences at the beginning of the article
            # (first few sentences often contain key information)
            if sentences.index(sentence) < 3:
                score += 2
            
            # Boost score for sentences with quotes (often contain key information)
            if '"' in sentence or "'" in sentence:
                score += 1
            
            # Boost score for sentences with numbers (often contain key statistics)
            if any(char.isdigit() for char in sentence):
                score += 1
            
            # Add the scored sentence to results
            scored_sentences.append((sentence, score))
        
        return scored_sentences
    
    def _format_sentence(self, sentence):
        """
        Format a sentence for readability as a key point.
        
        Args:
            sentence (str): The sentence to format
            
        Returns:
            str: Formatted sentence
        """
        # Ensure the sentence has proper punctuation
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        
        return sentence
