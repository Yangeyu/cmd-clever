"""Tests for the config module"""

import unittest
from unittest.mock import patch
from argparse import Namespace
from ccc.config import Config

class TestConfig(unittest.TestCase):
    """Test cases for Config class"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = Config()
        self.assertEqual(config.model, "gpt-4")
        self.assertEqual(config.api_base, "https://api.openai.com/v1")
        self.assertFalse(config.debug)
    
    def test_config_from_args(self):
        """Test configuration from command line arguments"""
        args = Namespace(
            api_key="test-key",
            model="gpt-3.5-turbo",
            api_base="https://custom-api.com",
            verbose=True
        )
        
        config = Config.from_args(args)
        self.assertEqual(config.api_key, "test-key")
        self.assertEqual(config.model, "gpt-3.5-turbo")
        self.assertEqual(config.api_base, "https://custom-api.com")
        self.assertTrue(config.debug)
    
    @patch.dict('os.environ', {
        'AI_API_KEY': 'env-key',
        'AI_MODEL': 'env-model',
        'AI_API_BASE': 'env-base'
    })
    def test_config_from_env(self):
        """Test configuration from environment variables"""
        config = Config()
        self.assertEqual(config.api_key, "env-key")
        self.assertEqual(config.model, "env-model")
        self.assertEqual(config.api_base, "env-base")

if __name__ == '__main__':
    unittest.main() 