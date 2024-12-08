
"""
commandline.py

This module provides a command-line interface for collecting article information
from the user and creating an Article object.

Functions:
    get_article_info(): Prompts the user for article details and returns an Article object.
"""
import article

def start(db, filename="citations.txt"):
    """ Starts the command-line interface. """

    print("Welcome to the citation database!")
    print("Commands: new, list, tag, save, load, quit")
    while True:
        command = input("Enter a command: ")
        if command == "new":
            info = get_article_info()
            db.add_citation(info)
        elif command == "list":
            print("Article Information:")
            # Listaa viitteet tietokannasta simpplisiti, jotta tägit voidaan liittää helpommin
            # lyhenne, otsikko, vuosi, tagit
            print_citation_list(db)
        elif command == "tag": # Tägätään jokin viite.
            # Anna viitteen lyhenne
            cite_key = input("Enter the citation key: ")
            # Anna tägi
            tags = input("Enter the tags: ").split(",")
            # Haetaan viite
            citation = db.get_one_citation(cite_key)
            # Lisätään tägit
            for tag in tags:
                citation.add_tag(tag.strip())
     
        elif command == "save":
            db.save_to_file(filename)
            print(f"Citations saved.")
        elif command == "load":
            db.load_from_file(filename)
            print(f"Citations loaded.")
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
    tags = input("Enter tags separated by commas: ").split(",")

    article_obj = article.Article(author, title, journal, year)
    # Tags doesn't save in database
    for tag in tags:
        article_obj.add_tag(tag.strip())

    return article_obj

def print_citation_list(db):
    """Prints the list of citations in the database."""
    for citation in db.get_citations():
        print(citation)
