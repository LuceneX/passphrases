"""
Passphrases package for generating and managing secure passphrases.

This package follows Model-View-Controller (MVC) architecture:
- Models: Business logic and data handling
- Views: User interface and presentation
- Controllers: Application logic coordination
"""

__version__ = "0.1.0"

# Import main components for easy access
from .controllers.application_controller import ApplicationController
from .controllers.passphrase_controller import PassphraseController
from .controllers.password_controller import PasswordController
from .models.passphrase_model import PassphraseModel
from .models.password_model import PasswordModel
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
    Generate a passphrase using default settings.
    
    Args:
        **kwargs: Passphrase generation parameters
        
    Returns:
        str: Generated passphrase
    """
    result = _default_app.generate_quick_passphrase(**kwargs)
    return result.get('passphrase', 'Error generating passphrase')


def generate_password(**kwargs) -> str:
    """
    Generate a password using default settings.
    
    Args:
        **kwargs: Password generation parameters
        
    Returns:
        str: Generated password
    """
    result = _default_app.generate_quick_password(**kwargs)
    return result.get('password', 'Error generating password')


def run_interactive() -> None:
    """
    Run the application in interactive mode.
    """
    _default_app.run_interactive_mode()


def demo() -> None:
    """
    Run a demonstration of the application capabilities.
    """
    _default_app.demo_generation()


# Export main components
__all__ = [
    'hello_world',
    'generate_passphrase', 
    'generate_password',
    'run_interactive',
    'demo',
    'ApplicationController',
    'PassphraseController',
    'PasswordController',
    'PassphraseModel',
    'PasswordModel',
    'WordRepository',
    'CLIView'
]


if __name__ == "__main__":
    print(hello_world())