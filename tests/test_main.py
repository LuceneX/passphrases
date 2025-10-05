"""
Tests for the passphrases package.
"""

import pytest
from passphrases import hello_world
from passphrases.main import generate_passphrase, generate_password


def test_hello_world():
    """Test the hello_world function."""
    result = hello_world()
    assert isinstance(result, str)
    assert "Hello, World!" in result


def test_generate_passphrase():
    """Test passphrase generation."""
    passphrase = generate_passphrase()
    assert isinstance(passphrase, str)
    assert len(passphrase.split("-")) == 4
    
    # Test custom parameters
    passphrase = generate_passphrase(word_count=3, separator="_")
    assert len(passphrase.split("_")) == 3


def test_generate_password():
    """Test password generation."""
    password = generate_password()
    assert isinstance(password, str)
    assert len(password) == 12
    
    # Test custom length
    password = generate_password(length=8)
    assert len(password) == 8


def test_generate_password_invalid():
    """Test password generation with invalid parameters."""
    with pytest.raises(ValueError):
        generate_password(
            include_uppercase=False,
            include_lowercase=False,
            include_digits=False,
            include_symbols=False
        )