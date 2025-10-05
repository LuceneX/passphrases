"""
Passphrase controller - Handles passphrase generation requests.
"""

from typing import Optional, Dict, Any
from ..models.passphrase_model import PassphraseModel
from ..models.word_repository import WordRepository
from ..views.cli_view import CLIView


class PassphraseController:
    """
    Controller for managing passphrase generation operations.
    """
    
    def __init__(
        self,
        model: Optional[PassphraseModel] = None,
        view: Optional[CLIView] = None,
        word_repository: Optional[WordRepository] = None
    ):
        """
        Initialize the passphrase controller.
        
        Args:
            model: Passphrase model instance
            view: CLI view instance
            word_repository: Word repository instance
        """
        self.word_repository = word_repository or WordRepository()
        self.model = model or PassphraseModel(self.word_repository)
        self.view = view or CLIView()
    
    def generate_passphrase(
        self,
        word_count: Optional[int] = None,
        separator: Optional[str] = None,
        capitalize: bool = True,
        include_numbers: bool = False
    ) -> Dict[str, Any]:
        """
        Generate a passphrase and return the result.
        
        Args:
            word_count: Number of words
            separator: Word separator
            capitalize: Whether to capitalize words
            include_numbers: Whether to include numbers
            
        Returns:
            Dict containing passphrase and metadata
        """
        try:
            # Generate passphrase
            passphrase = self.model.generate(
                word_count=word_count,
                separator=separator,
                capitalize=capitalize,
                include_numbers=include_numbers
            )
            
            # Calculate metadata
            actual_word_count = word_count or self.model.default_word_count
            entropy = self.model.estimate_entropy(actual_word_count)
            strength = self.model.get_strength_rating(actual_word_count)
            
            return {
                'passphrase': passphrase,
                'word_count': actual_word_count,
                'entropy': entropy,
                'strength': strength,
                'separator': separator or self.model.default_separator,
                'capitalized': capitalize,
                'includes_numbers': include_numbers
            }
            
        except ValueError as e:
            return {
                'error': str(e)
            }
    
    def generate_and_display_passphrase(
        self,
        word_count: Optional[int] = None,
        separator: Optional[str] = None,
        capitalize: bool = True,
        include_numbers: bool = False
    ) -> bool:
        """
        Generate a passphrase and display it using the view.
        
        Args:
            word_count: Number of words
            separator: Word separator
            capitalize: Whether to capitalize words
            include_numbers: Whether to include numbers
            
        Returns:
            bool: True if successful, False if there was an error
        """
        result = self.generate_passphrase(
            word_count=word_count,
            separator=separator,
            capitalize=capitalize,
            include_numbers=include_numbers
        )
        
        if 'error' in result:
            self.view.display_error(result['error'])
            return False
        
        self.view.display_passphrase(
            passphrase=result['passphrase'],
            word_count=result['word_count'],
            entropy=result['entropy'],
            strength=result['strength']
        )
        
        return True
    
    def generate_bulk_passphrases(self, count: int, **kwargs) -> list:
        """
        Generate multiple passphrases.
        
        Args:
            count: Number of passphrases to generate
            **kwargs: Additional parameters for passphrase generation
            
        Returns:
            List of generated passphrases
        """
        passphrases = []
        
        for _ in range(count):
            result = self.generate_passphrase(**kwargs)
            if 'error' not in result:
                passphrases.append(result['passphrase'])
        
        return passphrases
    
    def display_bulk_passphrases(self, count: int, **kwargs) -> None:
        """
        Generate and display multiple passphrases.
        
        Args:
            count: Number of passphrases to generate
            **kwargs: Additional parameters for passphrase generation
        """
        try:
            if count < 1 or count > 100:
                self.view.display_error("Count must be between 1 and 100")
                return
            
            passphrases = self.generate_bulk_passphrases(count, **kwargs)
            
            if passphrases:
                self.view.display_bulk_generation(passphrases, "Passphrase")
            else:
                self.view.display_error("Failed to generate passphrases")
                
        except Exception as e:
            self.view.display_error(f"Error generating passphrases: {str(e)}")
    
    def get_word_repository_info(self) -> Dict[str, Any]:
        """
        Get information about the word repository.
        
        Returns:
            Dict containing repository information
        """
        return {
            'word_count': self.word_repository.get_word_count(),
            'sample_words': self.word_repository.get_all_words()[:10]
        }
    
    def display_word_repository_info(self) -> None:
        """Display word repository information using the view."""
        info = self.get_word_repository_info()
        self.view.display_word_repository_stats(
            word_count=info['word_count'],
            sample_words=info['sample_words']
        )
    
    def add_custom_words(self, words: list) -> bool:
        """
        Add custom words to the repository.
        
        Args:
            words: List of words to add
            
        Returns:
            bool: True if successful
        """
        try:
            self.word_repository.add_words(words)
            return True
        except Exception:
            return False
    
    def validate_parameters(
        self,
        word_count: Optional[int] = None,
        separator: Optional[str] = None
    ) -> Optional[str]:
        """
        Validate passphrase generation parameters.
        
        Args:
            word_count: Number of words to validate
            separator: Separator to validate
            
        Returns:
            Error message if invalid, None if valid
        """
        try:
            if word_count is not None:
                self.model._validate_word_count(word_count)
            
            if separator is not None and len(separator) > 5:
                return "Separator cannot be longer than 5 characters"
            
            return None
            
        except ValueError as e:
            return str(e)