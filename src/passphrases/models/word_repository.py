"""
Word repository - Manages word data for passphrase generation using NLTK corpus.
"""

from typing import List, Optional, Set
import secrets
import string


class WordRepository:
    """
    Repository class for managing word collections used in passphrase generation.
    Uses NLTK corpus as primary source with fallback to built-in words.
    """
    
    def __init__(self, custom_words: Optional[List[str]] = None, min_length: int = 3, max_length: int = 12):
        """
        Initialize the word repository.
        
        Args:
            custom_words: Optional custom word list. If None, uses NLTK corpus.
            min_length: Minimum word length to include
            max_length: Maximum word length to include
        """
        self.min_length = min_length
        self.max_length = max_length
        self._words = custom_words or self._load_nltk_words()
    
    def _load_nltk_words(self) -> List[str]:
        """
        Load words from NLTK corpus with fallback to built-in words.
        
        Returns:
            List[str]: Filtered word collection
        """
        try:
            import nltk
            from nltk.corpus import words
            
            # Try to use the words corpus
            try:
                word_set = set(words.words())
            except LookupError:
                # Download the words corpus if not available
                nltk.download('words', quiet=True)
                word_set = set(words.words())
            
            # Filter words by length and alphabetic characters only
            filtered_words = [
                word.lower() for word in word_set
                if (self.min_length <= len(word) <= self.max_length and 
                    word.isalpha() and 
                    word.islower())
            ]
            
            # Remove duplicates and sort
            filtered_words = sorted(list(set(filtered_words)))
            
            if len(filtered_words) < 100:  # Fallback if too few words
                return self._get_fallback_words()
            
            return filtered_words
            
        except ImportError:
            # NLTK not available, use fallback
            return self._get_fallback_words()
        except Exception:
            # Any other error, use fallback
            return self._get_fallback_words()
    
    def _get_fallback_words(self) -> List[str]:
        """
        Get fallback word list when NLTK is not available.
        
        Returns:
            List[str]: Fallback collection of common English words
        """
        fallback_words = [
            # Common English words suitable for passphrases
            "able", "about", "above", "across", "after", "again", "against", "all", "almost", "alone",
            "along", "already", "also", "although", "always", "among", "another", "any", "anyone", "anything",
            "anywhere", "are", "area", "around", "back", "based", "became", "because", "become", "been",
            "before", "began", "being", "below", "between", "both", "bring", "but", "came", "can",
            "come", "could", "did", "different", "down", "during", "each", "early", "even", "every",
            "example", "far", "few", "find", "first", "for", "found", "from", "get", "give",
            "good", "great", "group", "hand", "hard", "has", "have", "hear", "help", "here",
            "high", "home", "how", "however", "include", "into", "its", "just", "know", "large",
            "last", "later", "learn", "left", "level", "life", "line", "list", "live", "local",
            "long", "look", "made", "make", "man", "many", "may", "member", "might", "most",
            "move", "much", "must", "name", "need", "never", "new", "next", "not", "now",
            "number", "off", "old", "once", "only", "open", "other", "over", "own", "part",
            "people", "place", "point", "present", "program", "put", "right", "run", "said", "same",
            "school", "see", "seem", "several", "should", "show", "small", "some", "something", "still",
            "such", "system", "take", "than", "that", "the", "their", "them", "then", "there",
            "these", "they", "thing", "think", "this", "those", "through", "time", "today", "together",
            "too", "turn", "two", "under", "until", "use", "used", "using", "very", "want",
            "water", "way", "well", "were", "what", "when", "where", "which", "while", "who",
            "will", "with", "within", "without", "work", "world", "would", "write", "year", "years"
        ]
        
        # Filter by length requirements
        return [word for word in fallback_words 
                if self.min_length <= len(word) <= self.max_length]
    
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