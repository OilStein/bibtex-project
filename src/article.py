"""Module for article object"""

import citation

class Article(citation.Citation):
    """Class for article object"""
    def __init__(self, authors, title, journal, year):
        super().__init__(title, authors, year)
        self.journal = journal
        self.doi = None

    def __str__(self):
        return f"{self.cite_key}, {self.title}, {self.author}, {self.journal}, {self.year}, {self.tags}"



    def print_as_bibtex(self):
        """Prints the article in BibTeX format."""
        return (
            f'@article{{{self.cite_key},\n'
            f'\tauthor = "{self.author}",\n'
            f'\ttitle = "{self.title}",\n'
            f'\tjournal = "{self.journal}",\n'
            f'\tyear = "{self.year}"\n'
            f'}}'
        )


def main(): #pragma: no cover
    """Main function"""
    authors = "John Doe"
    title = "Sample Article"
    journal = "Journal of Testing"
    year = 2023
    article = Article(authors, title, journal, year)
    article.add_tag("test")
    print(article)
    print(article.print_as_bibtex())

if __name__ == "__main__": #pragma: no cover
    main()
