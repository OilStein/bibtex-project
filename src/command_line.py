
"""
commandline.py

This module provides a command-line interface for collecting article information
from the user and creating an Article object.

Functions:
    get_article_info(): Prompts the user for article details and returns an Article object.
"""
import article
import database

db = database.Citations()

def get_article_info():
    """
    Prompts the user for article details and returns an Article object.
    """

    title = input("Enter the article title: ")
    author = input("Enter the author(s): ")
    journal = input("Enter the journal name: ")
    year = input("Enter the publication year: ")

    article_obj = article.Article(title, author, journal, year)

    return article_obj

if __name__ == "__main__":
    info = get_article_info()
    db.add_citation(info)
    print("Article Information:")
    for citation in db.get_citations():
        print(citation)
