"""Module for arcitle object"""

import citation

class Article(citation.Citation):
    """Class for article object"""
    def __init__(self, authors, title, journal, year):
        super().__init__(title, authors, year)
        self.journal = journal
        self.doi = None

    def __str__(self):
        return f"{self.title}, {self.author}, {self.journal}, {self.year}"
    
    def print_as_bibtex(self):
        """Prints the article in BibTeX format."""
        return f"@article{{,\n\tauthor = {{{self.author}}},\n\ttitle = {{{self.title}}},\n\tjournal = {{{self.journal}}},\n\tyear = {{{self.year}}}\n}}"
