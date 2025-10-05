"""
Console formatter - Handles formatting output for console display.
"""

from typing import Dict, Any, Optional
import sys


class ConsoleFormatter:
    """
    Handles formatting and displaying output to the console.
    """
    
    def __init__(self, use_colors: bool = True):
        """
        Initialize the console formatter.
        
        Args:
            use_colors: Whether to use ANSI color codes
        """
        self.use_colors = use_colors and sys.stdout.isatty()
        
        # ANSI color codes
        self.colors = {
            'reset': '\033[0m',
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'bold': '\033[1m',
            'underline': '\033[4m'
        }
    
    def colorize(self, text: str, color: str) -> str:
        """
        Apply color formatting to text.
        
        Args:
            text: Text to colorize
            color: Color name
            
        Returns:
            str: Colored text if colors are enabled, otherwise plain text
        """
        if not self.use_colors or color not in self.colors:
            return text
        
        return f"{self.colors[color]}{text}{self.colors['reset']}"
    
    def format_title(self, title: str) -> str:
        """
        Format a title with styling.
        
        Args:
            title: Title text
            
        Returns:
            str: Formatted title
        """
        return self.colorize(f"\n=== {title} ===\n", 'bold')
    
    def format_success(self, message: str) -> str:
        """
        Format a success message.
        
        Args:
            message: Success message
            
        Returns:
            str: Formatted success message
        """
        return self.colorize(f"✓ {message}", 'green')
    
    def format_error(self, message: str) -> str:
        """
        Format an error message.
        
        Args:
            message: Error message
            
        Returns:
            str: Formatted error message
        """
        return self.colorize(f"✗ Error: {message}", 'red')
    
    def format_warning(self, message: str) -> str:
        """
        Format a warning message.
        
        Args:
            message: Warning message
            
        Returns:
            str: Formatted warning message
        """
        return self.colorize(f"⚠ Warning: {message}", 'yellow')
    
    def format_info(self, message: str) -> str:
        """
        Format an info message.
        
        Args:
            message: Info message
            
        Returns:
            str: Formatted info message
        """
        return self.colorize(f"ℹ {message}", 'cyan')
    
    def format_generated_item(self, label: str, value: str, strength: Optional[str] = None) -> str:
        """
        Format a generated passphrase or password with metadata.
        
        Args:
            label: Label for the item (e.g., "Passphrase", "Password")
            value: The generated value
            strength: Optional strength rating
            
        Returns:
            str: Formatted output
        """
        lines = []
        lines.append(self.colorize(f"{label}:", 'bold'))
        lines.append(f"  {self.colorize(value, 'green')}")
        
        if strength:
            color = self._get_strength_color(strength)
            lines.append(f"  Strength: {self.colorize(strength, color)}")
        
        return "\n".join(lines)
    
    def _get_strength_color(self, strength: str) -> str:
        """
        Get the appropriate color for a strength rating.
        
        Args:
            strength: Strength rating
            
        Returns:
            str: Color name
        """
        strength_lower = strength.lower()
        
        if 'very weak' in strength_lower or 'weak' in strength_lower:
            return 'red'
        elif 'fair' in strength_lower:
            return 'yellow'
        elif 'good' in strength_lower:
            return 'blue'
        elif 'strong' in strength_lower or 'very strong' in strength_lower:
            return 'green'
        else:
            return 'white'
    
    def format_statistics(self, stats: Dict[str, Any]) -> str:
        """
        Format statistics information.
        
        Args:
            stats: Dictionary of statistics
            
        Returns:
            str: Formatted statistics
        """
        lines = [self.colorize("Statistics:", 'bold')]
        
        for key, value in stats.items():
            formatted_key = key.replace('_', ' ').title()
            lines.append(f"  {formatted_key}: {self.colorize(str(value), 'cyan')}")
        
        return "\n".join(lines)
    
    def print_output(self, message: str, end: str = '\n') -> None:
        """
        Print a message to stdout.
        
        Args:
            message: Message to print
            end: Line ending character
        """
        print(message, end=end)
    
    def print_error(self, message: str) -> None:
        """
        Print an error message to stderr.
        
        Args:
            message: Error message to print
        """
        print(self.format_error(message), file=sys.stderr)