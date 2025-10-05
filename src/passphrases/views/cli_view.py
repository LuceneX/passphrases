"""
CLI View - Command line interface presentation layer.
"""

from typing import Dict, Any, Optional
from .console_formatter import ConsoleFormatter


class CLIView:
    """
    Command-line interface view for displaying passphrases and passwords.
    """
    
    def __init__(self, formatter: Optional[ConsoleFormatter] = None):
        """
        Initialize the CLI view.
        
        Args:
            formatter: Console formatter instance. Creates default if None.
        """
        self.formatter = formatter or ConsoleFormatter()
    
    def display_welcome(self) -> None:
        """Display welcome message."""
        title = "Passphrases Generator"
        self.formatter.print_output(self.formatter.format_title(title))
        self.formatter.print_output(
            self.formatter.format_info("Generate secure passphrases and passwords")
        )
    
    def display_passphrase(
        self,
        passphrase: str,
        word_count: int,
        word_pool_size: int
    ) -> None:
        """
        Display a generated passphrase with metadata.
        
        Args:
            passphrase: The generated passphrase
            word_count: Number of words used
            word_pool_size: Size of available word pool
        """
        output = self.formatter.format_generated_item("Passphrase", passphrase)
        self.formatter.print_output(output)
        
        stats = {
            'word_count': word_count,
            'character_count': len(passphrase),
            'word_pool_size': word_pool_size
        }
        
        self.formatter.print_output(self.formatter.format_statistics(stats))
    

    
    def display_bulk_passphrases(self, passphrases: list) -> None:
        """
        Display multiple generated passphrases.
        
        Args:
            passphrases: List of generated passphrases
        """
        title = "Generated Passphrases"
        self.formatter.print_output(self.formatter.format_title(title))
        
        for i, passphrase in enumerate(passphrases, 1):
            self.formatter.print_output(f"{i:2d}. {self.formatter.colorize(passphrase, 'green')}")
    
    def display_error(self, error_message: str) -> None:
        """
        Display an error message.
        
        Args:
            error_message: Error message to display
        """
        self.formatter.print_error(error_message)
    
    def display_success(self, message: str) -> None:
        """
        Display a success message.
        
        Args:
            message: Success message to display
        """
        self.formatter.print_output(self.formatter.format_success(message))
    
    def display_info(self, message: str) -> None:
        """
        Display an informational message.
        
        Args:
            message: Info message to display
        """
        self.formatter.print_output(self.formatter.format_info(message))
    
    def display_help(self) -> None:
        """Display help information."""
        help_text = """
Available Commands:
  generate passphrase [options]  - Generate a secure passphrase
  bulk generate <count>          - Generate multiple passphrases
  
Options:
  --words N          - Set number of words in passphrase (default: 4)
  --separator CHAR   - Set word separator (default: -)
  --no-caps          - Don't capitalize words
  --include-numbers  - Add numbers to passphrase words
  --min-length N     - Minimum word length (default: 3)
  --max-length N     - Maximum word length (default: 12)
  
Examples:
  generate passphrase --words 5 --separator _
  generate passphrase --words 3 --no-caps
  bulk generate 10
        """
        
        self.formatter.print_output(self.formatter.format_title("Help"))
        self.formatter.print_output(help_text.strip())
    
    def display_word_repository_stats(self, word_count: int, sample_words: list) -> None:
        """
        Display word repository statistics.
        
        Args:
            word_count: Total number of words available
            sample_words: Sample of available words
        """
        self.formatter.print_output(self.formatter.format_title("Word Repository"))
        
        stats = {
            'total_words': word_count,
            'sample_words': ', '.join(sample_words[:5]) + ('...' if len(sample_words) > 5 else '')
        }
        
        self.formatter.print_output(self.formatter.format_statistics(stats))
    

    
    def prompt_input(self, message: str) -> str:
        """
        Prompt user for input.
        
        Args:
            message: Prompt message
            
        Returns:
            str: User input
        """
        try:
            return input(f"{self.formatter.colorize(message, 'yellow')} ")
        except (KeyboardInterrupt, EOFError):
            self.formatter.print_output("\nOperation cancelled.")
            return ""