"""Module for article object"""

import citation

class Article(citation.Citation):
    """Class for article object"""
    def __init__(self, authors, title, journal, year):
        super().__init__(title, authors, year)
        self.journal = journal
        self.doi = None

    def __str__(self):
        return f"{self.title}, {self.author}, {self.journal}, {self.year}"

    def generate_cite_key(self):
        """Generates a citation key for the article."""
        authors = self.author.split(" and") # BibTeX separates names with ' and'.
        surnames = ""
        for author in authors:
            surnames += author.split(' ')[-1]
        key = f"{surnames}{self.year}"
        return key

    def print_as_bibtex(self):
        """Prints the article in BibTeX format."""
        return (
            f'@article{{{self.generate_cite_key()},\n'
            f'\tauthor = "{self.author}",\n'
            f'\ttitle = "{self.title}",\n'
            f'\tjournal = "{self.journal}",\n'
            f'\tyear = "{self.year}"\n'
            f'}}'
        )


def main():
    """Main function"""
    authors = "John Doe"
    title = "Sample Article"
    journal = "Journal of Testing"
    year = 2023
    article = Article(authors, title, journal, year)
    print(article.print_as_bibtex())

if __name__ == "__main__":
    main()
