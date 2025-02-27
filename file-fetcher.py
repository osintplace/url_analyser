"""
File fetcher for retrieving article content from local files.
"""

import os
from news_analyzer.fetchers.base_fetcher import BaseFetcher


class FileFetcher(BaseFetcher):
    """
    Fetches content from local files.
    
    Supports different file encodings and handles common file errors.
    """
    
    def __init__(self, encoding='utf-8'):
        """
        Initialize the file fetcher with custom settings.
        
        Args:
            encoding (str): File encoding to use when reading files
        """
        self.encoding = encoding
    
    def fetch(self, filepath):
        """
        Fetch content from a local file.
        
        Args:
            filepath (str): Path to the file to read
            
        Returns:
            str: The content of the file
            
        Raises:
            FileNotFoundError: If the file does not exist
            PermissionError: If the file cannot be read due to permissions
            ValueError: If the filepath is invalid
        """
        # Validate filepath
        if not filepath:
            raise ValueError("Filepath cannot be empty")
        
        # Check if file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Check if it's a file (not a directory)
        if not os.path.isfile(filepath):
            raise ValueError(f"Not a file: {filepath}")
        
        try:
            # Read the file
            with open(filepath, 'r', encoding=self.encoding) as file:
                return file.read()
        
        except UnicodeDecodeError:
            # Try to read with a different encoding if UTF-8 fails
            try:
                with open(filepath, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                raise ValueError(f"Error reading file with alternative encoding: {str(e)}")
        
        except Exception as e:
            # Convert other exceptions to more specific errors
            if isinstance(e, PermissionError):
                raise
            raise ValueError(f"Error reading file: {str(e)}")
    
    def fetch_with_metadata(self, filepath):
        """
        Fetch content along with file metadata.
        
        Args:
            filepath (str): Path to the file
            
        Returns:
            dict: Dictionary with content and metadata
        """
        # Get content
        content = self.fetch(filepath)
        
        # Get file metadata
        file_stats = os.stat(filepath)
        
        return {
            "content": content,
            "size": file_stats.st_size,
            "modified": file_stats.st_mtime,
            "created": file_stats.st_ctime,
            "path": os.path.abspath(filepath),
            "filename": os.path.basename(filepath),
            "extension": os.path.splitext(filepath)[1]
        }
