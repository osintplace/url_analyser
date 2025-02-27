"""
Base fetcher module defining the interface for all content fetchers.
"""

from abc import ABC, abstractmethod


class BaseFetcher(ABC):
    """
    Abstract base class for all content fetchers.
    
    Defines the interface that concrete fetcher implementations must follow.
    """
    
    @abstractmethod
    def fetch(self, source):
        """
        Fetch content from a source.
        
        Args:
            source: The source to fetch content from (URL, file path, etc.)
            
        Returns:
            str: The content from the source
            
        Raises:
            Exception: If content cannot be fetched
        """
        pass
