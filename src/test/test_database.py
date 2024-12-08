""" Test the database module """
import unittest
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

        with patch("builtins.open", mock_open()) as mocked_file:
            self.db.save_to_file(self.filename)

            mocked_file.assert_called_with(self.filename, 'w', encoding= "utf-8")

            handle = mocked_file()
            handle.write.assert_any_call(
                f"{article_obj.generate_cite_key()}, Test title, Test person, "
                "Test journal, 2024, ['']\n"
            )
