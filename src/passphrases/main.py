"""
Main module for passphrase functionality.
"""

from typing import List, Optional
import secrets
import string


def generate_passphrase(
    word_count: int = 4,
    separator: str = "-",
    capitalize: bool = True
) -> str:
    """
    Generate a simple passphrase using random words.
    
    Args:
        word_count: Number of words in the passphrase
        separator: Character to separate words
        capitalize: Whether to capitalize the first letter of each word
    
    Returns:
        str: Generated passphrase
    """
    # Simple word list for demo purposes
    words = [
        "apple", "banana", "cherry", "dragon", "elephant", "forest",
        "galaxy", "harbor", "island", "jungle", "kitchen", "laptop",
        "mountain", "nature", "ocean", "planet", "question", "rainbow",
        "sunset", "thunder", "universe", "valley", "winter", "xenon",
        "yellow", "zephyr"
    ]
    
    selected_words = [secrets.choice(words) for _ in range(word_count)]
    
    if capitalize:
        selected_words = [word.capitalize() for word in selected_words]
    
    return separator.join(selected_words)


def generate_password(
    length: int = 12,
    include_uppercase: bool = True,
    include_lowercase: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True
) -> str:
    """
    Generate a secure random password.
    
    Args:
        length: Length of the password
        include_uppercase: Include uppercase letters
        include_lowercase: Include lowercase letters
        include_digits: Include digits
        include_symbols: Include symbols
    
    Returns:
        str: Generated password
    """
    character_pool = ""
    
    if include_lowercase:
        character_pool += string.ascii_lowercase
    if include_uppercase:
        character_pool += string.ascii_uppercase
    if include_digits:
        character_pool += string.digits
    if include_symbols:
        character_pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not character_pool:
        raise ValueError("At least one character type must be included")
    
    return "".join(secrets.choice(character_pool) for _ in range(length))