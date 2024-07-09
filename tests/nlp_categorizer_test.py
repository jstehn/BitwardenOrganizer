import sys
import os
# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from unittest.mock import patch, MagicMock
from nlp_categorizer import NLPCategorizer

class TestNLPCategorizer(unittest.TestCase):
    def setUp(self):
        self.categorizer = NLPCategorizer()

    @patch('nlp_categorizer.language_v1.LanguageServiceClient')
    def test_init(self, mock_client):
        self.assertIsNotNone(self.categorizer.client)
        self.assertEqual(self.categorizer.categories, {})
        self.assertEqual(self.categorizer.entries, {})

    @patch('nlp_categorizer.NLPCategorizer.fetch_website_content', return_value="Test content")
    @patch('nlp_categorizer.NLPCategorizer.classify_html', return_value=[MagicMock(name="/Test/Category")])
    def test_categorize_websites_with_content(self, mock_classify, mock_fetch):
        mock_classify.return_value[0].name = "/Test/Category"
        self.categorizer.entries = {"TestID": ["https://example.com"]}
        self.categorizer.categorize_websites()
        print(dict(self.categorizer.categories))
        self.assertIn("Test", self.categorizer.categories)

    def test_categorize_websites_no_content(self):
        self.categorizer.entries = {"TestID": ["https://example.com"]}
        with patch('nlp_categorizer.NLPCategorizer.fetch_website_content', return_value=""):
            self.categorizer.categorize_websites()
            self.assertEqual(self.categorizer.categories, {})

    @patch('nlp_categorizer.NLPCategorizer.fetch_website_content', return_value="a" * 1000001)
    @patch('nlp_categorizer.NLPCategorizer.classify_html', return_value=[MagicMock(name="Test/Category")])
    def test_categorize_websites_large_content(self, mock_classify, mock_fetch):
        self.categorizer.entries = {"TestID": ["https://example.com"]}
        self.categorizer.categorize_websites()
        mock_classify.assert_called_once()
        args, _ = mock_classify.call_args
        self.assertTrue(len(args[0]) <= 900000, "Content should be truncated to 900000 characters")

if __name__ == '__main__':
    unittest.main()