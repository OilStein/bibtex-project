import unittest
from article import Article
class TestArticle(unittest.TestCase):
    def test_constructor_and_to_string(self):
        authors = "T. Case"
        title = "Testing the Article-class"
        journal = "Journal of Test cases"
        year = "2024"
        article_obj = Article(authors, title, journal, year)
        self.assertEqual(str(article_obj), f"{article_obj.generate_cite_key()}, {title}, {authors}, {journal}, {year}, {[]}")

    def test_generate_cite_key_one_author(self):
        authors = "T. Case"
        title = "Testing the Article-class"
        journal = "Journal of Test cases"
        year = "2024"
        article_obj = Article(authors, title, journal, year)
        self.assertEqual(article_obj.generate_cite_key(), "Case2024")

    def test_generate_cite_key_multiple_authors(self):
        authors = "T. Case and O. Ther and A. Uthors"
        title = "Testing the Article-class"
        journal = "Journal of Test cases"
        year = "2024"
        article_obj = Article(authors, title, journal, year)
        self.assertEqual(article_obj.generate_cite_key(), "CaseTherUthors2024")

    def test_print_as_bibtex_one_author(self):
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
        self.assertEqual(article_obj.print_as_bibtex(), article_as_bibtex)

    def test_print_as_bibtex_multiple_authors(self):
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
        self.assertEqual(article_obj.print_as_bibtex(), article_as_bibtex)