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

# Generate a password
passphrases password

# Generate with custom options
passphrases passphrase --words 5 --separator _
passphrases password --length 16 --no-symbols

# Generate multiple items
passphrases passphrase --count 5
passphrases password --count 10

# Run demo
passphrases demo
```

### Python API

```python
# Simple usage (backwards compatible)
from passphrases import hello_world, generate_passphrase, generate_password

print(hello_world())
passphrase = generate_passphrase()
password = generate_password()

# Interactive mode
from passphrases import run_interactive
run_interactive()

# Using MVC components directly
from passphrases import ApplicationController

app = ApplicationController()
app.run_interactive_mode()

# Advanced usage with models
from passphrases.models import PassphraseModel, WordRepository
from passphrases.views import CLIView

# Custom word repository
custom_words = ['secure', 'random', 'words', 'here']
repo = WordRepository(custom_words)
model = PassphraseModel(repo)
view = CLIView()

passphrase = model.generate(word_count=3, separator='-')
print(passphrase)
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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.