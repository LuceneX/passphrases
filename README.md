# Passphrases

A Python library for secure passphrase generation using **NLTK corpus** and built with **Model-View-Controller (MVC)** architecture.

## Features

- **NLTK Corpus Integration**: Uses the comprehensive NLTK words corpus (175,000+ English words)
- **Flexible Generation**: Customizable word count, separators, capitalization, and number inclusion
- **MVC Architecture**: Clean, maintainable, and extensible codebase
- **Importable Library**: Easy to integrate into other applications
- **CLI Interface**: Command-line tool for direct usage
- **Fallback Support**: Works even without NLTK installation

## Architecture

This library follows the MVC design pattern:

- **Models** (`models/`): Business logic and data handling
  - `PassphraseModel`: Core passphrase generation logic
  - `WordRepository`: NLTK corpus integration and word management
  
- **Views** (`views/`): User interface and presentation
  - `CLIView`: Command-line interface
  - `ConsoleFormatter`: Colored output formatting
  
- **Controllers** (`controllers/`): Application coordination
  - `ApplicationController`: Main application orchestration
  - `PassphraseController`: Passphrase generation operations

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/passphrases.git
cd passphrases

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e .[dev]
```

## Usage

### Command Line Interface

```bash
# Interactive mode
passphrases

# Generate a passphrase
passphrases passphrase

# Generate with custom options
passphrases passphrase --words 5 --separator _
passphrases passphrase --words 3 --no-caps --include-numbers

# Word length filtering
passphrases passphrase --min-length 5 --max-length 8

# Generate multiple passphrases
passphrases passphrase --count 10

# Run demo
passphrases demo
```

### Python API (Library Usage)

```python
# Simple usage - perfect for integration
from passphrases import generate_passphrase

# Basic generation
passphrase = generate_passphrase()
print(passphrase)  # "Magnificent-Serendipity-Crystalline-Ephemeral"

# Custom parameters  
passphrase = generate_passphrase(
    word_count=3, 
    separator='_', 
    capitalize=False,
    include_numbers=True
)
print(passphrase)  # "magnificent12_serendipity47_crystalline89"

# Using MVC components directly for advanced control
from passphrases.models import PassphraseModel, WordRepository

# Custom word filtering
repo = WordRepository(min_length=6, max_length=10)
model = PassphraseModel(repo)

passphrase = model.generate(
    word_count=4, 
    separator='-', 
    capitalize=True
)
print(passphrase)

# Interactive mode in applications
from passphrases import run_interactive
run_interactive()
```

### Word Sources

The library uses multiple word sources with automatic fallback:

1. **Primary**: NLTK corpus (`nltk.corpus.words`) - ~175,000 English words
2. **Secondary**: Built-in curated word list - ~100 common English words
3. **Custom**: User-provided word lists

```python
# Using custom words
from passphrases.models import WordRepository, PassphraseModel

custom_words = ['quantum', 'nexus', 'cipher', 'matrix', 'protocol']
repo = WordRepository(custom_words)
model = PassphraseModel(repo)
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src/ tests/
```

### Type Checking

```bash
mypy src/
```

## Why This Library?

- **No Password Strength Evaluation**: Focuses purely on generation, letting other tools handle strength analysis
- **NLTK Integration**: Leverages the most comprehensive English word corpus available
- **Library-First Design**: Built for integration into other applications
- **Clean Architecture**: MVC pattern makes it easy to extend and maintain
- **Extensive Word Pool**: 175,000+ words provide excellent entropy and variety
- **Flexible API**: Simple functions for basic use, full MVC access for advanced needs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.