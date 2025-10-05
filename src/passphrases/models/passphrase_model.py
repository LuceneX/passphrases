"""
Passphrase model - Business logic for passphrase generation.
"""

from typing import List, Optional
from .word_repository import WordRepository


class PassphraseModel:
    """
    Model class for passphrase generation and validation.
    """
    
    def __init__(self, word_repository: Optional[WordRepository] = None):
        """
        Initialize the passphrase model.
        
        Args:
            word_repository: Repository for word data. If None, creates default repository.
        """
        self.word_repository = word_repository or WordRepository()
        self.min_word_count = 2
        self.max_word_count = 10
        self.default_word_count = 4
        self.default_separator = "-"
    
    def generate(
        self,
        word_count: Optional[int] = None,
        separator: Optional[str] = None,
        capitalize: bool = True,
        include_numbers: bool = False
    ) -> str:
        """
        Generate a passphrase with the specified parameters.
        
        Args:
            word_count: Number of words (uses default if None)
            separator: Character to separate words (uses default if None)
            capitalize: Whether to capitalize first letter of each word
            include_numbers: Whether to append random numbers to words
            
        Returns:
            str: Generated passphrase
            
        Raises:
            ValueError: If word_count is invalid
        """
        word_count = word_count or self.default_word_count
        separator = separator or self.default_separator
        
        self._validate_word_count(word_count)
        
        # Get random words
        words = self.word_repository.get_random_words(word_count)
        
        # Apply transformations
        if capitalize:
            words = [word.capitalize() for word in words]
        
        if include_numbers:
            import secrets
            words = [f"{word}{secrets.randbelow(100):02d}" for word in words]
        
        return separator.join(words)
    
    def _validate_word_count(self, word_count: int) -> None:
        """
        Validate the word count parameter.
        
        Args:
            word_count: Number of words to validate
            
        Raises:
            ValueError: If word count is invalid
        """
        if not isinstance(word_count, int):
            raise ValueError("Word count must be an integer")
        
        if word_count < self.min_word_count:
            raise ValueError(f"Word count must be at least {self.min_word_count}")
        
        if word_count > self.max_word_count:
            raise ValueError(f"Word count cannot exceed {self.max_word_count}")
        
        available_words = self.word_repository.get_word_count()
        if word_count > available_words:
            raise ValueError(f"Cannot generate {word_count} words from {available_words} available words")
    
    def estimate_entropy(self, word_count: Optional[int] = None) -> float:
        """
        Estimate the entropy (bits) of a passphrase with the given word count.
        
        Args:
            word_count: Number of words (uses default if None)
            
        Returns:
            float: Estimated entropy in bits
        """
        import math
        
        word_count = word_count or self.default_word_count
        available_words = self.word_repository.get_word_count()
        
        # Entropy = log2(possible_combinations)
        # For passphrases: possible_combinations = available_words ^ word_count
        entropy = word_count * math.log2(available_words)
        
        return entropy
    
    def get_strength_rating(self, word_count: Optional[int] = None) -> str:
        """
        Get a human-readable strength rating for a passphrase.
        
        Args:
            word_count: Number of words (uses default if None)
            
        Returns:
            str: Strength rating (Weak, Fair, Good, Strong, Very Strong)
        """
        entropy = self.estimate_entropy(word_count)
        
        if entropy < 30:
            return "Weak"
        elif entropy < 50:
            return "Fair"
        elif entropy < 70:
            return "Good"
        elif entropy < 90:
            return "Strong"
        else:
            return "Very Strong"