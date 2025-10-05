# Passphrases

A Python project for passphrase generation and management.

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

```python
from passphrases import hello_world

hello_world()
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