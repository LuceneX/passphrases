"""
Tests for the passphrases package (NLTK-based passphrase generation library).
"""

import pytest
from passphrases import hello_world, generate_passphrase
from passphrases.main import generate_passphrase as main_generate_passphrase
from passphrases.models.passphrase_model import PassphraseModel
from passphrases.models.word_repository import WordRepository
from passphrases.controllers.application_controller import ApplicationController


class TestBackwardsCompatibility:
    """Test backwards compatibility with original API."""
    
    def test_hello_world(self):
        """Test the hello_world function."""
        result = hello_world()
        assert isinstance(result, str)
        assert "Hello, World!" in result
    
    def test_generate_passphrase_package_level(self):
        """Test passphrase generation from package level."""
        passphrase = generate_passphrase()
        assert isinstance(passphrase, str)
        assert len(passphrase.split("-")) >= 3  # Should have at least 3 words
        
        # Test custom parameters
        passphrase = generate_passphrase(word_count=3, separator="_")
        assert len(passphrase.split("_")) == 3
    
    def test_main_generate_passphrase(self):
        """Test passphrase generation from main module."""
        passphrase = main_generate_passphrase()
        assert isinstance(passphrase, str)
        assert len(passphrase.split("-")) >= 3  # Should have at least 3 words


class TestWordRepository:
    """Test the word repository model."""
    
    def test_initialization(self):
        """Test repository initialization."""
        repo = WordRepository()
        assert repo.get_word_count() > 0
        
        custom_words = ['test', 'custom', 'words']
        custom_repo = WordRepository(custom_words)
        assert custom_repo.get_word_count() == 3
    
    def test_get_random_words(self):
        """Test getting random words."""
        repo = WordRepository()
        words = repo.get_random_words(3)
        assert len(words) == 3
        assert len(set(words)) == 3  # Should be unique
    
    def test_add_remove_words(self):
        """Test adding and removing words."""
        repo = WordRepository(['test'])
        initial_count = repo.get_word_count()
        
        repo.add_words(['new', 'words'])
        assert repo.get_word_count() == initial_count + 2
        
        assert repo.remove_word('test') is True
        assert repo.remove_word('nonexistent') is False


class TestPassphraseModel:
    """Test the passphrase model."""
    
    def test_initialization(self):
        """Test model initialization."""
        model = PassphraseModel()
        assert model.default_word_count == 4
        assert model.default_separator == "-"
    
    def test_generate_passphrase(self):
        """Test passphrase generation."""
        model = PassphraseModel()
        passphrase = model.generate()
        
        assert isinstance(passphrase, str)
        assert len(passphrase.split("-")) == 4
    
    def test_generate_with_parameters(self):
        """Test passphrase generation with custom parameters."""
        model = PassphraseModel()
        
        passphrase = model.generate(word_count=3, separator="_", capitalize=False)
        words = passphrase.split("_")
        assert len(words) == 3
        assert all(word.islower() for word in words)
    
    def test_validate_word_count(self):
        """Test word count validation."""
        model = PassphraseModel()
        
        with pytest.raises(ValueError):
            model._validate_word_count(1)  # Too low
        
        with pytest.raises(ValueError):
            model._validate_word_count(100)  # Too high
    
    def test_word_pool_info(self):
        """Test word pool information."""
        model = PassphraseModel()
        word_pool_size = model.get_word_pool_size()
        assert word_pool_size > 0


class TestApplicationController:
    """Test the application controller."""
    
    def test_initialization(self):
        """Test controller initialization."""
        app = ApplicationController()
        assert app.passphrase_controller is not None
        assert app.word_repository is not None
        assert app.passphrase_model is not None
    
    def test_quick_passphrase_generation(self):
        """Test quick passphrase generation method."""
        app = ApplicationController()
        
        passphrase_result = app.generate_quick_passphrase()
        assert 'passphrase' in passphrase_result
        assert 'error' not in passphrase_result
        assert 'word_count' in passphrase_result
        assert 'word_pool_size' in passphrase_result
    
    def test_hello_world_mvc(self):
        """Test MVC version of hello world."""
        app = ApplicationController()
        result = app.hello_world()
        assert "Hello, World!" in result