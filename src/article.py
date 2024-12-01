"""Module for arcitle object"""

import citation

class Article(citation.Citation):
    """Class for article object"""
    def __init__(self, authors, title, journal, year):
        super().__init__(title, authors, year)
        self.journal = journal
        self.doi = None

    def __str__(self):
        return f"{super().__str__()}. {self.journal}."
