"""
Sentiment analyzer module for determining the emotional tone of news articles.
"""


class SentimentAnalyzer:
    """
    Analyzes the sentiment of article text using term frequency analysis.
    
    This is a simple rule-based sentiment analyzer that looks for specific
    terms associated with different emotional tones in news reporting.
    """
    
    def __init__(self):
        """Initialize with term lists for different sentiment categories"""
        # Terms that indicate positive sentiment
        self.positive_terms = [
            'celebrated', 'acclaimed', 'praised', 'honored', 'respected',
            'admired', 'appreciated', 'commended', 'acclaimed', 'successful',
            'achievement', 'breakthrough', 'triumph', 'victory', 'win',
            'positive', 'beneficial', 'favorable', 'promising', 'encouraging',
            'optimistic', 'progress', 'improvement', 'growth', 'recovery',
            'accomplishment', 'excellence', 'outstanding', 'remarkable',
            'genius', 'legendary', 'icon', 'influential', 'inspiring',
            'innovator', 'pioneer', 'visionary', 'revolutionary', 'leader',
            'talented', 'brilliant', 'exceptional', 'extraordinary'
        ]
        
        # Terms that indicate negative sentiment
        self.negative_terms = [
            'tragic', 'devastating', 'critical', 'negative', 'concerning',
            'worrying', 'disappointing', 'unfortunate', 'sad', 'grim',
            'failure', 'problem', 'issue', 'challenge', 'crisis',
            'disaster', 'catastrophe', 'emergency', 'accident', 'incident',
            'controversy', 'scandal', 'conflict', 'dispute', 'debate',
            'criticism', 'complaint', 'objection', 'protest', 'opposition',
            'dead', 'died', 'killed', 'deceased', 'fatal', 'death',
            'injured', 'wounded', 'hurt', 'damaged', 'destroyed', 'lost',
            'criminal', 'illegal', 'accused', 'alleged', 'charged', 'convicted'
        ]
        
        # Terms that indicate neutral, factual reporting
        self.neutral_terms = [
            'reported', 'announced', 'stated', 'said', 'told', 'explained',
            'described', 'informed', 'confirmed', 'indicated', 'revealed',
            'noted', 'mentioned', 'added', 'continued', 'concluded',
            'according to', 'based on', 'as per', 'cited', 'referenced',
            'data', 'statistics', 'figures', 'numbers', 'percentage',
            'research', 'study', 'analysis', 'survey', 'report',
            'investigation', 'examination', 'assessment', 'evaluation',
            'development', 'change', 'increase', 'decrease', 'rise', 'fall',
            'update', 'situation', 'circumstance', 'condition', 'status'
        ]
    
    def analyze(self, text):
        """
        Analyze the sentiment of the article text.
        
        Args:
            text (str): The article text to analyze
            
        Returns:
            tuple: (sentiment_labels, sentiment_analysis)
                - sentiment_labels is a list of overall sentiment categories
                - sentiment_analysis is a list of detailed analysis statements
        """
        # Convert text to lowercase for case-insensitive matching
        lowercase_text = text.lower()
        
        # Count occurrences of terms from each category
        positive_count = sum(lowercase_text.count(term.lower()) for term in self.positive_terms)
        negative_count = sum(lowercase_text.count(term.lower()) for term in self.negative_terms)
        neutral_count = sum(lowercase_text.count(term.lower()) for term in self.neutral_terms)
        
        # Determine overall sentiment categories based on term counts
        sentiment_labels = []
        
        # If there are many positive terms, consider it "Commemorative" or "Positive"
        if positive_count > 5:
            if "obituary" in lowercase_text or "tribute" in lowercase_text:
                sentiment_labels.append("Commemorative")
            else:
                sentiment_labels.append("Positive")
        
        # If there are many negative terms, consider it "Somber" or "Negative"
        if negative_count > 5:
            if "died" in lowercase_text or "death" in lowercase_text:
                sentiment_labels.append("Somber")
            else:
                sentiment_labels.append("Negative")
        
        # If neutral terms dominate, consider it primarily "Factual"
        if neutral_count > positive_count and neutral_count > negative_count:
            sentiment_labels.append("Factual")
        
        # Special case for obituaries and tributes
        if "obituary" in lowercase_text or "tribute" in lowercase_text:
            sentiment_labels.append("Respectful")
        
        # Default sentiment if no strong signals are detected
        if not sentiment_labels:
            sentiment_labels = ["Neutral", "Factual"]
        
        # Generate detailed analysis statements
        sentiment_analysis = self._generate_analysis_statements(
            text, sentiment_labels, positive_count, negative_count, neutral_count
        )
        
        return sentiment_labels, sentiment_analysis
    
    def _generate_analysis_statements(self, text, sentiment_labels, positive_count, 
                                      negative_count, neutral_count):
        """
        Generate detailed analysis statements based on detected sentiment.
        
        Args:
            text (str): The article text
            sentiment_labels (list): The detected sentiment labels
            positive_count (int): Count of positive terms
            negative_count (int): Count of negative terms
            neutral_count (int): Count of neutral terms
            
        Returns:
            list: List of analysis statements
        """
        lowercase_text = text.lower()
        analysis_statements = []
        
        # Add specific analysis statements for each detected sentiment type
        if "Factual" in sentiment_labels:
            analysis_statements.append(
                "The article maintains a neutral, factual tone focused on reporting events"
            )
        
        if "Commemorative" in sentiment_labels:
            analysis_statements.append(
                "The tone becomes celebratory and respectful when discussing achievements and legacy"
            )
        
        if "Somber" in sentiment_labels:
            analysis_statements.append(
                "The article adopts a somber tone when describing the circumstances"
            )
        
        if "Positive" in sentiment_labels:
            analysis_statements.append(
                "The article presents developments in a positive light with optimistic framing"
            )
        
        if "Negative" in sentiment_labels:
            analysis_statements.append(
                "The article highlights concerns and problems with a critical perspective"
            )
        
        # Add analysis of quotes if present
        if '"' in text:
            if positive_count > negative_count:
                analysis_statements.append(
                    "Quotes in the article generally express positive or supportive viewpoints"
                )
            elif negative_count > positive_count:
                analysis_statements.append(
                    "Quotes in the article generally express critical or concerned viewpoints"
                )
        
        # Add analysis of balance if appropriate
        if abs(positive_count - negative_count) < 3 and neutral_count > (positive_count + negative_count) / 2:
            analysis_statements.append(
                "The article presents a balanced perspective with multiple viewpoints"
            )
        
        # Look for specific patterns in obituaries or tributes
        if "tribute" in lowercase_text:
            analysis_statements.append(
                "Tributes included in the article express admiration for contributions and accomplishments"
            )
        
        return analysis_statements
