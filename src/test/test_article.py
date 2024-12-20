""" This module contains the tests for the Article class. """
import unittest
from article import Article
class TestArticle(unittest.TestCase):
    """ This class contains the tests for the Article class. """
    def test_constructor_and_to_string(self):
        """ This method tests the constructor and the to_string method of the Article class. """
        authors = "T. Case"
        title = "Testing the Article-class"
        journal = "Journal of Test cases"
        year = "2024"
        article_obj = Article(authors, title, journal, year)
        self.assertEqual(
            str(article_obj),
            f"{article_obj.generate_cite_key()}, {title}, {authors}, {journal}, {year}, {['']}"
        )

    def test_generate_cite_key_one_author(self):
        """ This method tests the generate_cite_key method of the Article class with one author. """
        authors = "T. Case"
        title = "Testing the Article-class"
        journal = "Journal of Test cases"
        year = "2024"
        article_obj = Article(authors, title, journal, year)
        self.assertEqual(article_obj.generate_cite_key(), "Case2024")

    def test_generate_cite_key_multiple_authors(self):
        """
        This method tests the generate_cite_key method of the Article class with multiple authors.
        """
        authors = "T. Case and O. Ther and A. Uthors"
        title = "Testing the Article-class"
        journal = "Journal of Test cases"
        year = "2024"
        article_obj = Article(authors, title, journal, year)
        self.assertEqual(article_obj.generate_cite_key(), "CaseTherUthors2024")

    def test_print_as_bibtex_one_author(self):
        """ This method tests the print_as_bibtex method of the Article class with one author. """
        authors = "T. Case"
        title = "Testing the Article-class"
        journal = "Journal of Test cases"
        year = "2024"
        article_obj = Article(authors, title, journal, year)
        article_as_bibtex = """@article{Case2024,
\tauthor = "T. Case",
\ttitle = "Testing the Article-class",
\tjournal = "Journal of Test cases",
\tyear = "2024"
}"""
        self.assertEqual(article_obj.to_bibtex(), article_as_bibtex)

    def test_print_as_bibtex_multiple_authors(self):
        """ 
        This method tests the print_as_bibtex method of the Article class with multiple authors.
        """
        authors = "T. Case and O. Ther and A. Uthors"
        title = "Testing the Article-class"
        journal = "Journal of Test cases"
        year = "2024"
        article_obj = Article(authors, title, journal, year)
        article_as_bibtex = """@article{CaseTherUthors2024,
\tauthor = "T. Case and O. Ther and A. Uthors",
\ttitle = "Testing the Article-class",
\tjournal = "Journal of Test cases",
\tyear = "2024"
}"""
        self.assertEqual(article_obj.to_bibtex(), article_as_bibtex)
