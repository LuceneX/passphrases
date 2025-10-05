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


def generate_password(
    length: int = 12,
    include_uppercase: bool = True,
    include_lowercase: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True
) -> str:
    """
    Generate a secure random password.
    
    Args:
        length: Length of the password
        include_uppercase: Include uppercase letters
        include_lowercase: Include lowercase letters
        include_digits: Include digits
        include_symbols: Include symbols
    
    Returns:
        str: Generated password
    """
    app = ApplicationController()
    result = app.generate_quick_password(
        length=length,
        include_uppercase=include_uppercase,
        include_lowercase=include_lowercase,
        include_digits=include_digits,
        include_symbols=include_symbols
    )
    return result.get('password', 'Error generating password')


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
  %(prog)s password                # Generate password
  %(prog)s passphrase --words 5    # 5-word passphrase
  %(prog)s password --length 16    # 16-character password
  %(prog)s demo                    # Run demonstration
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        choices=['passphrase', 'password', 'demo', 'interactive'],
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
    
    # Password options
    parser.add_argument(
        '--length',
        type=int,
        default=12,
        help='Password length (default: 12)'
    )
    parser.add_argument(
        '--no-uppercase',
        action='store_true',
        help='Exclude uppercase letters'
    )
    parser.add_argument(
        '--no-lowercase',
        action='store_true',
        help='Exclude lowercase letters'
    )
    parser.add_argument(
        '--no-digits',
        action='store_true',
        help='Exclude digits'
    )
    parser.add_argument(
        '--no-symbols',
        action='store_true',
        help='Exclude symbols'
    )
    parser.add_argument(
        '--exclude-ambiguous',
        action='store_true',
        help='Exclude ambiguous characters (0, O, l, I, etc.)'
    )
    
    # Bulk generation
    parser.add_argument(
        '--count',
        type=int,
        default=1,
        help='Number of items to generate (default: 1)'
    )
    
    args = parser.parse_args()
    
    # Create application controller
    app = ApplicationController()
    
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
        
        elif args.command == 'password':
            # Generate password(s)
            if args.count == 1:
                app.password_controller.generate_and_display_password(
                    length=args.length,
                    include_uppercase=not args.no_uppercase,
                    include_lowercase=not args.no_lowercase,
                    include_digits=not args.no_digits,
                    include_symbols=not args.no_symbols,
                    exclude_ambiguous=args.exclude_ambiguous
                )
            else:
                app.password_controller.display_bulk_passwords(
                    count=args.count,
                    length=args.length,
                    include_uppercase=not args.no_uppercase,
                    include_lowercase=not args.no_lowercase,
                    include_digits=not args.no_digits,
                    include_symbols=not args.no_symbols,
                    exclude_ambiguous=args.exclude_ambiguous
                )
    
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()