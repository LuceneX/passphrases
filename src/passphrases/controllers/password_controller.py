"""
Password controller - Handles password generation requests.
"""

from typing import Optional, Dict, Any
from ..models.password_model import PasswordModel
from ..views.cli_view import CLIView


class PasswordController:
    """
    Controller for managing password generation operations.
    """
    
    def __init__(
        self,
        model: Optional[PasswordModel] = None,
        view: Optional[CLIView] = None
    ):
        """
        Initialize the password controller.
        
        Args:
            model: Password model instance
            view: CLI view instance
        """
        self.model = model or PasswordModel()
        self.view = view or CLIView()
    
    def generate_password(
        self,
        length: Optional[int] = None,
        include_uppercase: bool = True,
        include_lowercase: bool = True,
        include_digits: bool = True,
        include_symbols: bool = True,
        exclude_ambiguous: bool = False
    ) -> Dict[str, Any]:
        """
        Generate a password and return the result.
        
        Args:
            length: Password length
            include_uppercase: Include uppercase letters
            include_lowercase: Include lowercase letters
            include_digits: Include digits
            include_symbols: Include symbols
            exclude_ambiguous: Exclude ambiguous characters
            
        Returns:
            Dict containing password and metadata
        """
        try:
            # Generate password
            password = self.model.generate(
                length=length,
                include_uppercase=include_uppercase,
                include_lowercase=include_lowercase,
                include_digits=include_digits,
                include_symbols=include_symbols,
                exclude_ambiguous=exclude_ambiguous
            )
            
            # Calculate metadata
            actual_length = length or self.model.default_length
            entropy = self.model.estimate_entropy(
                length=actual_length,
                include_uppercase=include_uppercase,
                include_lowercase=include_lowercase,
                include_digits=include_digits,
                include_symbols=include_symbols,
                exclude_ambiguous=exclude_ambiguous
            )
            strength = self.model.get_strength_rating(
                length=actual_length,
                include_uppercase=include_uppercase,
                include_lowercase=include_lowercase,
                include_digits=include_digits,
                include_symbols=include_symbols,
                exclude_ambiguous=exclude_ambiguous
            )
            
            return {
                'password': password,
                'length': actual_length,
                'entropy': entropy,
                'strength': strength,
                'character_types': {
                    'uppercase': include_uppercase,
                    'lowercase': include_lowercase,
                    'digits': include_digits,
                    'symbols': include_symbols
                },
                'exclude_ambiguous': exclude_ambiguous
            }
            
        except ValueError as e:
            return {
                'error': str(e)
            }
    
    def generate_and_display_password(
        self,
        length: Optional[int] = None,
        include_uppercase: bool = True,
        include_lowercase: bool = True,
        include_digits: bool = True,
        include_symbols: bool = True,
        exclude_ambiguous: bool = False
    ) -> bool:
        """
        Generate a password and display it using the view.
        
        Args:
            length: Password length
            include_uppercase: Include uppercase letters
            include_lowercase: Include lowercase letters
            include_digits: Include digits
            include_symbols: Include symbols
            exclude_ambiguous: Exclude ambiguous characters
            
        Returns:
            bool: True if successful, False if there was an error
        """
        result = self.generate_password(
            length=length,
            include_uppercase=include_uppercase,
            include_lowercase=include_lowercase,
            include_digits=include_digits,
            include_symbols=include_symbols,
            exclude_ambiguous=exclude_ambiguous
        )
        
        if 'error' in result:
            self.view.display_error(result['error'])
            return False
        
        self.view.display_password(
            password=result['password'],
            length=result['length'],
            entropy=result['entropy'],
            strength=result['strength']
        )
        
        return True
    
    def generate_bulk_passwords(self, count: int, **kwargs) -> list:
        """
        Generate multiple passwords.
        
        Args:
            count: Number of passwords to generate
            **kwargs: Additional parameters for password generation
            
        Returns:
            List of generated passwords
        """
        passwords = []
        
        for _ in range(count):
            result = self.generate_password(**kwargs)
            if 'error' not in result:
                passwords.append(result['password'])
        
        return passwords
    
    def display_bulk_passwords(self, count: int, **kwargs) -> None:
        """
        Generate and display multiple passwords.
        
        Args:
            count: Number of passwords to generate
            **kwargs: Additional parameters for password generation
        """
        try:
            if count < 1 or count > 100:
                self.view.display_error("Count must be between 1 and 100")
                return
            
            passwords = self.generate_bulk_passwords(count, **kwargs)
            
            if passwords:
                self.view.display_bulk_generation(passwords, "Password")
            else:
                self.view.display_error("Failed to generate passwords")
                
        except Exception as e:
            self.view.display_error(f"Error generating passwords: {str(e)}")
    
    def validate_parameters(
        self,
        length: Optional[int] = None,
        include_uppercase: bool = True,
        include_lowercase: bool = True,
        include_digits: bool = True,
        include_symbols: bool = True
    ) -> Optional[str]:
        """
        Validate password generation parameters.
        
        Args:
            length: Password length to validate
            include_uppercase: Include uppercase letters
            include_lowercase: Include lowercase letters
            include_digits: Include digits
            include_symbols: Include symbols
            
        Returns:
            Error message if invalid, None if valid
        """
        try:
            if length is not None:
                self.model._validate_length(length)
            
            # Check if at least one character type is enabled
            if not any([include_uppercase, include_lowercase, include_digits, include_symbols]):
                return "At least one character type must be enabled"
            
            return None
            
        except ValueError as e:
            return str(e)
    
    def get_complexity_analysis(
        self,
        length: Optional[int] = None,
        include_uppercase: bool = True,
        include_lowercase: bool = True,
        include_digits: bool = True,
        include_symbols: bool = True,
        exclude_ambiguous: bool = False
    ) -> Dict[str, Any]:
        """
        Get detailed complexity analysis for password parameters.
        
        Returns:
            Dict containing complexity analysis
        """
        actual_length = length or self.model.default_length
        
        # Build character pool to analyze
        character_pool = self.model._build_character_pool(
            include_uppercase, include_lowercase,
            include_digits, include_symbols, exclude_ambiguous
        )
        
        entropy = self.model.estimate_entropy(
            length=actual_length,
            include_uppercase=include_uppercase,
            include_lowercase=include_lowercase,
            include_digits=include_digits,
            include_symbols=include_symbols,
            exclude_ambiguous=exclude_ambiguous
        )
        
        strength = self.model.get_strength_rating(
            length=actual_length,
            include_uppercase=include_uppercase,
            include_lowercase=include_lowercase,
            include_digits=include_digits,
            include_symbols=include_symbols,
            exclude_ambiguous=exclude_ambiguous
        )
        
        # Calculate time to crack estimates (very rough approximations)
        combinations = len(character_pool) ** actual_length
        
        return {
            'length': actual_length,
            'character_pool_size': len(character_pool),
            'total_combinations': combinations,
            'entropy_bits': entropy,
            'strength_rating': strength,
            'character_types_enabled': sum([
                include_uppercase, include_lowercase,
                include_digits, include_symbols
            ])
        }