
"""
commandline.py

This module provides a command-line interface for collecting article information
from the user and creating an Article object.

Functions:
    get_article_info(): Prompts the user for article details and returns an Article object.
"""
import article

def start(db):
    """ Starts the command-line interface. """

    print("Welcome to the citation database!")
    print("Commands: new, list, quit")
    while True:
        command = input("Enter a command: ")
        if command == "new":
            info = get_article_info()
            db.add_citation(info)
        elif command == "list":
            print("Article Information:")
            for citation in db.get_citations():
                print(citation.print_as_bibtex())
        elif command == "quit":
            break
        else:
            print("Invalid command. Please try again.")


def get_article_info():
    """
    Prompts the user for article details and returns an Article object.
    """

    title = input("Enter the article title: ")
    author = input("Enter the author(s): ")
    journal = input("Enter the journal name: ")
    year = input("Enter the publication year: ")

    article_obj = article.Article(title, author, journal, year)

    return article_obj.print_as_bibtex()
