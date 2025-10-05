"""
Password model - Business logic for password generation.
"""

import secrets
import string
from typing import Set, Optional


class PasswordModel:
    """
    Model class for password generation and validation.
    """
    
    def __init__(self):
        """Initialize the password model with default settings."""
        self.min_length = 4
        self.max_length = 128
        self.default_length = 12
        
        # Character sets
        self.lowercase_chars = string.ascii_lowercase
        self.uppercase_chars = string.ascii_uppercase
        self.digit_chars = string.digits
        self.symbol_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
    def generate(
        self,
        length: Optional[int] = None,
        include_uppercase: bool = True,
        include_lowercase: bool = True,
        include_digits: bool = True,
        include_symbols: bool = True,
        exclude_ambiguous: bool = False
    ) -> str:
        """
        Generate a secure random password.
        
        Args:
            length: Length of the password (uses default if None)
            include_uppercase: Include uppercase letters
            include_lowercase: Include lowercase letters
            include_digits: Include digits
            include_symbols: Include symbols
            exclude_ambiguous: Exclude ambiguous characters (0, O, l, I, etc.)
            
        Returns:
            str: Generated password
            
        Raises:
            ValueError: If parameters are invalid
        """
        length = length or self.default_length
        
        self._validate_length(length)
        character_pool = self._build_character_pool(
            include_uppercase, include_lowercase, 
            include_digits, include_symbols, exclude_ambiguous
        )
        
        if not character_pool:
            raise ValueError("At least one character type must be included")
        
        # Generate password ensuring at least one character from each selected type
        password_chars = []
        
        # Add at least one character from each enabled character set
        required_chars = []
        if include_lowercase:
            chars = self._filter_ambiguous(self.lowercase_chars, exclude_ambiguous)
            if chars:
                required_chars.append(secrets.choice(chars))
        
        if include_uppercase:
            chars = self._filter_ambiguous(self.uppercase_chars, exclude_ambiguous)
            if chars:
                required_chars.append(secrets.choice(chars))
        
        if include_digits:
            chars = self._filter_ambiguous(self.digit_chars, exclude_ambiguous)
            if chars:
                required_chars.append(secrets.choice(chars))
        
        if include_symbols:
            chars = self._filter_ambiguous(self.symbol_chars, exclude_ambiguous)
            if chars:
                required_chars.append(secrets.choice(chars))
        
        # Fill the rest with random characters from the full pool
        remaining_length = length - len(required_chars)
        password_chars.extend(required_chars)
        password_chars.extend(
            secrets.choice(character_pool) for _ in range(remaining_length)
        )
        
        # Shuffle the characters to avoid predictable patterns
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def _validate_length(self, length: int) -> None:
        """
        Validate the password length.
        
        Args:
            length: Password length to validate
            
        Raises:
            ValueError: If length is invalid
        """
        if not isinstance(length, int):
            raise ValueError("Password length must be an integer")
        
        if length < self.min_length:
            raise ValueError(f"Password length must be at least {self.min_length}")
        
        if length > self.max_length:
            raise ValueError(f"Password length cannot exceed {self.max_length}")
    
    def _build_character_pool(
        self,
        include_uppercase: bool,
        include_lowercase: bool,
        include_digits: bool,
        include_symbols: bool,
        exclude_ambiguous: bool
    ) -> str:
        """
        Build the character pool based on the specified options.
        
        Returns:
            str: Character pool for password generation
        """
        pool = ""
        
        if include_lowercase:
            pool += self._filter_ambiguous(self.lowercase_chars, exclude_ambiguous)
        if include_uppercase:
            pool += self._filter_ambiguous(self.uppercase_chars, exclude_ambiguous)
        if include_digits:
            pool += self._filter_ambiguous(self.digit_chars, exclude_ambiguous)
        if include_symbols:
            pool += self._filter_ambiguous(self.symbol_chars, exclude_ambiguous)
        
        return pool
    
    def _filter_ambiguous(self, chars: str, exclude_ambiguous: bool) -> str:
        """
        Filter out ambiguous characters if requested.
        
        Args:
            chars: Character string to filter
            exclude_ambiguous: Whether to exclude ambiguous characters
            
        Returns:
            str: Filtered character string
        """
        if not exclude_ambiguous:
            return chars
        
        # Ambiguous characters that can be confused
        ambiguous = set('0O1lI|`')
        return ''.join(char for char in chars if char not in ambiguous)
    
    def estimate_entropy(
        self,
        length: Optional[int] = None,
        include_uppercase: bool = True,
        include_lowercase: bool = True,
        include_digits: bool = True,
        include_symbols: bool = True,
        exclude_ambiguous: bool = False
    ) -> float:
        """
        Estimate the entropy (bits) of a password with the given parameters.
        
        Args:
            length: Password length (uses default if None)
            include_uppercase: Include uppercase letters
            include_lowercase: Include lowercase letters
            include_digits: Include digits
            include_symbols: Include symbols
            exclude_ambiguous: Exclude ambiguous characters
            
        Returns:
            float: Estimated entropy in bits
        """
        import math
        
        length = length or self.default_length
        character_pool = self._build_character_pool(
            include_uppercase, include_lowercase,
            include_digits, include_symbols, exclude_ambiguous
        )
        
        if not character_pool:
            return 0.0
        
        # Entropy = length * log2(character_pool_size)
        entropy = length * math.log2(len(character_pool))
        
        return entropy
    
    def get_strength_rating(
        self,
        length: Optional[int] = None,
        include_uppercase: bool = True,
        include_lowercase: bool = True,
        include_digits: bool = True,
        include_symbols: bool = True,
        exclude_ambiguous: bool = False
    ) -> str:
        """
        Get a human-readable strength rating for a password.
        
        Returns:
            str: Strength rating (Very Weak, Weak, Fair, Good, Strong, Very Strong)
        """
        entropy = self.estimate_entropy(
            length, include_uppercase, include_lowercase,
            include_digits, include_symbols, exclude_ambiguous
        )
        
        if entropy < 25:
            return "Very Weak"
        elif entropy < 35:
            return "Weak"
        elif entropy < 50:
            return "Fair"
        elif entropy < 70:
            return "Good"
        elif entropy < 90:
            return "Strong"
        else:
            return "Very Strong"