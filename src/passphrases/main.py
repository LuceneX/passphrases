"""
Main entry point for the passphrases application.

This module provides command-line interface and backwards compatibility
with the original function signatures.
"""

import sys
import argparse
from typing import Optional

from .controllers.application_controller import ApplicationController


# Backwards compatibility functions (using original signatures)
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
    app = ApplicationController()
    result = app.generate_quick_passphrase(
        word_count=word_count,
        separator=separator,
        capitalize=capitalize
    )
    return result.get('passphrase', 'Error generating passphrase')





def main() -> None:
    """
    Main command-line interface entry point.
    """
    parser = argparse.ArgumentParser(
        description='Generate secure passphrases and passwords',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Interactive mode
  %(prog)s passphrase              # Generate passphrase
  %(prog)s passphrase --words 5    # 5-word passphrase
  %(prog)s passphrase --count 10   # Generate 10 passphrases
  %(prog)s demo                    # Run demonstration
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        choices=['passphrase', 'demo', 'interactive'],
        help='What to generate or run'
    )
    
    # Passphrase options
    parser.add_argument(
        '--words',
        type=int,
        default=4,
        help='Number of words in passphrase (default: 4)'
    )
    parser.add_argument(
        '--separator',
        default='-',
        help='Word separator for passphrase (default: -)'
    )
    parser.add_argument(
        '--no-caps',
        action='store_true',
        help='Do not capitalize words in passphrase'
    )
    parser.add_argument(
        '--include-numbers',
        action='store_true',
        help='Include numbers in passphrase words'
    )
    parser.add_argument(
        '--min-length',
        type=int,
        default=3,
        help='Minimum word length (default: 3)'
    )
    parser.add_argument(
        '--max-length',
        type=int,
        default=12,
        help='Maximum word length (default: 12)'
    )
    
    # Bulk generation
    parser.add_argument(
        '--count',
        type=int,
        default=1,
        help='Number of items to generate (default: 1)'
    )
    
    args = parser.parse_args()
    
    # Create application controller with custom word repository if needed
    word_repo = WordRepository(min_length=args.min_length, max_length=args.max_length)
    app = ApplicationController(word_repository=word_repo)
    
    try:
        if args.command is None or args.command == 'interactive':
            # Interactive mode
            app.run_interactive_mode()
        
        elif args.command == 'demo':
            # Demo mode
            app.demo_generation()
        
        elif args.command == 'passphrase':
            # Generate passphrase(s)
            if args.count == 1:
                app.passphrase_controller.generate_and_display_passphrase(
                    word_count=args.words,
                    separator=args.separator,
                    capitalize=not args.no_caps,
                    include_numbers=args.include_numbers
                )
            else:
                app.passphrase_controller.display_bulk_passphrases(
                    count=args.count,
                    word_count=args.words,
                    separator=args.separator,
                    capitalize=not args.no_caps,
                    include_numbers=args.include_numbers
                )
    
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()