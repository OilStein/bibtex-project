"""
commandline.py

This module provides a command-line interface for collecting article information
from the user and creating an Article object.

Functions:
    get_article_info(): Prompts the user for article details and returns an Article object.
"""
import article

# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
def start(db, filename="data/citations.txt"):
    """ Starts the command-line interface. """

    print("Welcome to the citation database!")
    print("Commands: new, list, tag, save, load, quit, edit, load bibtex, save bibtex")
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
        elif command == "edit":
            cite_key = input("Enter the citation key of the citation to edit: ")
            citation = db.get_one_citation(cite_key)
            if citation is None:
                print("Citation not found.")
                continue

            print("Leave the field blank to keep the current value.")
            new_title = input(f"Enter new title (current: {citation.title}): ") or citation.title
            new_author = input(
                f"Enter new author(s) (current: {citation.author}): ") or citation.author
            new_year = input(f"Enter new year (current: {citation.year}): ") or citation.year

            citation.title = new_title
            citation.author = new_author
            citation.year = new_year
            print("Citation updated successfully.")

        elif command == "tag": # Tägätään jokin viite.
            # Anna viitteen lyhenne
            cite_key = input("Enter the citation key: ")
            # Haetaan viite
            citation = db.get_one_citation(cite_key)
            if citation is None:
                print("Citation not found.")
                continue
            # Anna tägi
            tags = input("Enter the tags: ").split(",")
            # Lisätään tägit
            for tag in tags:
                citation.add_tag(tag.strip())

        elif command == "save":
            filename = input("Enter the filename: ")
            if filename == "":
                filename = "citations"
            db.save_to_file(f"data/{filename}.txt")

        elif command == "load":
            filename= input("Enter the filename: ")
            if filename == "":
                print("No filename entered.")
                continue
            db.load_from_file(f"data/{filename}")

        elif command == "save bibtex":
            filename = input("Enter the filename: ")
            if filename == "":
                filename = "bibtex"
            db.save_as_bibtex(f"data/{filename}.bib")

        elif command == "load bibtex":
            filename = input("Enter the filename: ")
            if filename == "":
                filename = "bibtex"
            db.load_from_bibtex(f"data/{filename}.bib")
        
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
        # Needs to be in this format for the tests to work. Otherwise comparing object to string.
        print(str(citation))
