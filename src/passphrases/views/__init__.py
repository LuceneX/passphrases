"""
Views package - Contains user interface and presentation logic.
"""

from .cli_view import CLIView
from .console_formatter import ConsoleFormatter

__all__ = ['CLIView', 'ConsoleFormatter']