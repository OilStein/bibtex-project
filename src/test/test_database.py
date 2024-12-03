import unittest
from database import Citations
from article import Article

class TestCitations(unittest.TestCase):
    def setUp(self):
        self.db = Citations()

    def test_constructor_creates_empty_citations(self):
        self.assertEqual(len(self.db.get_citations()), 0)

    def test_adding_citation(self):
        article_obj = Article("Testing in python", "T. Est and C. ase", "Journal of Tests", "2024")
        self.db.add_citation(article_obj)
        self.assertEqual(len(self.db.get_citations()), 1)
        self.assertEqual(self.db.get_citations()[0], article_obj)
