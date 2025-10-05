"""
Application controller - Main controller coordinating the entire application.
"""

from typing import Optional, List, Dict, Any
from ..models.passphrase_model import PassphraseModel
from ..models.word_repository import WordRepository
from ..views.cli_view import CLIView
from .passphrase_controller import PassphraseController


class ApplicationController:
    """
    Main application controller that coordinates passphrase generation operations.
    """
    
    def __init__(
        self,
        view: Optional[CLIView] = None,
        word_repository: Optional[WordRepository] = None
    ):
        """
        Initialize the application controller.
        
        Args:
            view: CLI view instance
            word_repository: Word repository instance
        """
        self.view = view or CLIView()
        self.word_repository = word_repository or WordRepository()
        
        # Initialize models
        self.passphrase_model = PassphraseModel(self.word_repository)
        
        # Initialize sub-controllers
        self.passphrase_controller = PassphraseController(
            model=self.passphrase_model,
            view=self.view,
            word_repository=self.word_repository
        )
    
    def run_interactive_mode(self) -> None:
        """
        Run the application in interactive mode.
        """
        self.view.display_welcome()
        
        while True:
            try:
                command = self.view.prompt_input("Enter command (help for options, quit to exit):").strip().lower()
                
                if not command:
                    continue
                
                if command in ['quit', 'exit', 'q']:
                    self.view.display_info("Goodbye!")
                    break
                elif command in ['help', 'h', '?']:
                    self.view.display_help()
                elif command.startswith('generate') or command.startswith('passphrase'):
                    self._generate_passphrase_interactive()
                elif command.startswith('bulk'):
                    self._handle_bulk_command(command)
                elif command == 'stats':
                    self._display_statistics()
                else:
                    self.view.display_error(f"Unknown command: {command}")
                    self.view.display_info("Type 'help' for available commands")
            
            except KeyboardInterrupt:
                self.view.display_info("\nGoodbye!")
                break
            except Exception as e:
                self.view.display_error(f"Unexpected error: {str(e)}")
    

    
    def _handle_bulk_command(self, command: str) -> None:
        """
        Handle bulk generation commands.
        
        Args:
            command: The full command string
        """
        parts = command.split()
        
        if len(parts) < 4:
            self.view.display_error("Usage: bulk generate <count> <type>")
            return
        
        try:
            count = int(parts[2])
            self.passphrase_controller.display_bulk_passphrases(count)
        
        except ValueError:
            self.view.display_error("Count must be a valid number")
        except IndexError:
            self.view.display_error("Usage: bulk generate <count>")
    
    def _generate_passphrase_interactive(self) -> None:
        """Generate passphrase with interactive prompts."""
        try:
            word_count_input = self.view.prompt_input("Number of words (default 4):")
            word_count = int(word_count_input) if word_count_input.strip() else None
            
            separator = self.view.prompt_input("Separator (default '-'):")
            separator = separator if separator.strip() else None
            
            capitalize_input = self.view.prompt_input("Capitalize words? (y/n, default y):")
            capitalize = capitalize_input.lower() not in ['n', 'no', 'false']
            
            numbers_input = self.view.prompt_input("Include numbers? (y/n, default n):")
            include_numbers = numbers_input.lower() in ['y', 'yes', 'true']
            
            # Validate parameters
            error = self.passphrase_controller.validate_parameters(word_count, separator)
            if error:
                self.view.display_error(error)
                return
            
            # Generate and display
            self.passphrase_controller.generate_and_display_passphrase(
                word_count=word_count,
                separator=separator,
                capitalize=capitalize,
                include_numbers=include_numbers
            )
            
        except ValueError:
            self.view.display_error("Invalid number for word count")
        except Exception as e:
            self.view.display_error(f"Error generating passphrase: {str(e)}")
    

    
    def _display_statistics(self) -> None:
        """Display application statistics."""
        self.passphrase_controller.display_word_repository_info()
    
    def generate_quick_passphrase(self, **kwargs) -> Dict[str, Any]:
        """
        Generate a passphrase with default or provided parameters.
        
        Args:
            **kwargs: Passphrase generation parameters
            
        Returns:
            Dict containing passphrase result
        """
        return self.passphrase_controller.generate_passphrase(**kwargs)
    

    
    def hello_world(self) -> str:
        """
        Backwards compatibility function.
        
        Returns:
            str: Welcome message
        """
        return "Hello, World! Welcome to the Passphrases project (MVC Architecture)!"
    
    def demo_generation(self) -> None:
        """
        Run a demonstration of the generation capabilities.
        """
        self.view.display_info("Demonstration Mode")
        
        # Generate sample passphrase
        passphrase_result = self.generate_quick_passphrase()
        if 'error' not in passphrase_result:
            self.view.display_passphrase(
                passphrase=passphrase_result['passphrase'],
                word_count=passphrase_result['word_count'],
                entropy=passphrase_result['entropy'],
                strength=passphrase_result['strength']
            )
        
        # Generate sample password
        password_result = self.generate_quick_password()
        if 'error' not in password_result:
            self.view.display_password(
                password=password_result['password'],
                length=password_result['length'],
                entropy=password_result['entropy'],
                strength=password_result['strength']
            )