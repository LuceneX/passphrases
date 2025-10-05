"""
Word repository - Manages word data for passphrase generation.
"""

from typing import List, Optional
import secrets


class WordRepository:
    """
    Repository class for managing word collections used in passphrase generation.
    """
    
    def __init__(self, custom_words: Optional[List[str]] = None):
        """
        Initialize the word repository.
        
        Args:
            custom_words: Optional custom word list. If None, uses default words.
        """
        self._words = custom_words or self._get_default_words()
    
    def _get_default_words(self) -> List[str]:
        """
        Get the default word list.
        
        Returns:
            List[str]: Default collection of words
        """
        return [
            "apple", "banana", "cherry", "dragon", "elephant", "forest",
            "galaxy", "harbor", "island", "jungle", "kitchen", "laptop",
            "mountain", "nature", "ocean", "planet", "question", "rainbow",
            "sunset", "thunder", "universe", "valley", "winter", "xenon",
            "yellow", "zephyr", "bridge", "castle", "diamond", "engine",
            "falcon", "guitar", "hammer", "iceberg", "jacket", "keychain",
            "lighthouse", "mirror", "network", "orange", "pencil", "quartz",
            "rocket", "silver", "tiger", "umbrella", "violet", "wizard"
        ]
    
    def get_random_words(self, count: int) -> List[str]:
        """
        Get a list of random words from the repository.
        
        Args:
            count: Number of words to retrieve
            
        Returns:
            List[str]: List of randomly selected words
            
        Raises:
            ValueError: If count is less than 1 or greater than available words
        """
        if count < 1:
            raise ValueError("Word count must be at least 1")
        if count > len(self._words):
            raise ValueError(f"Cannot select {count} words from {len(self._words)} available words")
        
        return secrets.SystemRandom().sample(self._words, count)
    
    def get_all_words(self) -> List[str]:
        """
        Get all words in the repository.
        
        Returns:
            List[str]: All available words
        """
        return self._words.copy()
    
    def add_words(self, words: List[str]) -> None:
        """
        Add words to the repository.
        
        Args:
            words: List of words to add
        """
        self._words.extend(word.lower().strip() for word in words if word.strip())
    
    def remove_word(self, word: str) -> bool:
        """
        Remove a word from the repository.
        
        Args:
            word: Word to remove
            
        Returns:
            bool: True if word was removed, False if not found
        """
        try:
            self._words.remove(word.lower().strip())
            return True
        except ValueError:
            return False
    
    def get_word_count(self) -> int:
        """
        Get the total number of words in the repository.
        
        Returns:
            int: Number of words available
        """
        return len(self._words)