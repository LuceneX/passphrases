"""
Passphrases - A Python library for secure passphrase generation using NLTK corpus.

This package follows Model-View-Controller (MVC) architecture:
- Models: Business logic and data handling (NLTK word repository, passphrase generation)
- Views: User interface and presentation (CLI, formatting)  
- Controllers: Application logic coordination (passphrase operations)
"""

__version__ = "0.1.0"

# Import main components for easy access
from .controllers.application_controller import ApplicationController
from .controllers.passphrase_controller import PassphraseController
from .models.passphrase_model import PassphraseModel
from .models.word_repository import WordRepository
from .views.cli_view import CLIView

# Create default application controller instance
_default_app = ApplicationController()


def hello_world() -> str:
    """
    A simple hello world function for backwards compatibility.
    
    Returns:
        str: A greeting message
    """
    return _default_app.hello_world()


def generate_passphrase(**kwargs) -> str:
    """
    Generate a passphrase using NLTK corpus words.
    
    Args:
        word_count: Number of words (default: 4)
        separator: Word separator (default: '-')
        capitalize: Whether to capitalize words (default: True)
        include_numbers: Whether to add numbers to words (default: False)
        
    Returns:
        str: Generated passphrase
        
    Example:
        >>> generate_passphrase(word_count=3, separator='_')
        'Apple_Mountain_Ocean'
    """
    result = _default_app.generate_quick_passphrase(**kwargs)
    return result.get('passphrase', 'Error generating passphrase')


def run_interactive() -> None:
    """
    Run the application in interactive mode.
    """
    _default_app.run_interactive_mode()


def demo() -> None:
    """
    Run a demonstration of the passphrase generation capabilities.
    """
    _default_app.demo_generation()


# Export main components
__all__ = [
    'hello_world',
    'generate_passphrase',
    'run_interactive', 
    'demo',
    'ApplicationController',
    'PassphraseController',
    'PassphraseModel',
    'WordRepository',
    'CLIView'
]


if __name__ == "__main__":
    print(hello_world())