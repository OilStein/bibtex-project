""" Test the database module """
import unittest
import json
from unittest.mock import patch, mock_open
from database import Citations
from article import Article

class TestCitations(unittest.TestCase):
    """ This class contains the tests for the Citations class. """
    def setUp(self):
        self.db = Citations()
        self.filename = "test_citations.txt"

    def test_constructor_creates_empty_citations(self):
        """Test that the constructor creates an empty list of citations"""
        self.assertEqual(len(self.db.get_citations()), 0)

    def test_adding_citation(self):
        """Test that citations can be added to the database """
        article_obj = Article("Testing in python", "T. Est and C. ase", "Journal of Tests", "2024")
        self.db.add_citation(article_obj)
        self.assertEqual(len(self.db.get_citations()), 1)
        self.assertEqual(self.db.get_citations()[0], article_obj)

    def test_save_to_file(self):
        """Test to save to a file"""
        article_obj = Article("Test person", "Test title", "Test journal", "2024")
        self.db.add_citation(article_obj)

        with patch(
            "builtins.open", mock_open()) as mocked_file, patch("json.dump") as mock_json_dump:
            self.db.save_to_file(self.filename)

            mocked_file.assert_called_with(self.filename, 'w', encoding= "utf-8")

            handle = mocked_file()
            mock_json_dump.assert_called_once_with(
                [article_obj.to_dict()], handle, indent=4
            )

    def test_load_from_file(self):
        """Test loading from a file"""
        mock_data = json.dumps([
            {
                "title": "Testaus",
                "author": "Testaaja",
                "year": "2024",
                "tags": ["test"],
                "cite_key": "Testaaja2024",
                "journal": "Testi lehti",
                "doi": None
            }
        ])

        db = Citations()

        with patch("builtins.open", mock_open(read_data=mock_data)):
            db.load_from_file("test.json")

        self.assertTrue(len(db.get_citations()) == 1)

        loaded_article = db.get_citations()[0]

        self.assertTrue(isinstance(loaded_article, Article))

        self.assertTrue(loaded_article.title == "Testaus")
        self.assertTrue(loaded_article.author == "Testaaja")
        self.assertTrue(loaded_article.year == "2024")
        self.assertTrue(loaded_article.tags == ["test"])
        self.assertTrue(loaded_article.journal == "Testi lehti")
        self.assertTrue(loaded_article.cite_key == "Testaaja2024")
        self.assertTrue(loaded_article.doi is None)
