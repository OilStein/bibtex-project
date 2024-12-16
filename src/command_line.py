"""
commandline.py

This module provides a command-line interface for collecting article information
from the user and creating an Article object.

Functions:
    get_article_info(): Prompts the user for article details and returns an Article object.
"""
import article
import citation

# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
def start(db):
    """ Starts the command-line interface. """

    print("Welcome to the citation database!")
    print("Commands: new, from doi, list, tag, save, load, quit, edit, load bibtex, save bibtex")
    while True:
        command = input("Enter a command: ")

        if command == "new":
            add_citation(db)
        elif command == "from doi":
            add_citation_doi(db)
        elif command == "list":
            list_citations(db)
        elif command == "edit":
            edit_citation(db)
        elif command == "tag":
            add_tag(db)
        elif command == "save":
            save_to_file(db, "citations")
        elif command == "load":
            load_from_file(db)
        elif command == "save bibtex":
            save_as_bibtex(db, 'bibtex')
        elif command == "load bibtex":
            load_from_bibtex(db, 'bibtex')
        elif command == "quit":
            break
        else:
            print("Invalid command. Please try again.")

def add_citation(db):
    """
    Asks the user for article information and adds it to the database.
    """
    article_obj = get_article_info()
    db.add_citation(article_obj)

def add_citation_doi(db):
    """
    Asks the user for article doi and adds it to the database.
    """
    doi = input("Give doi: ")
    article_obj = citation.Citation.from_doi(doi)
    print(f"Added article \"{article_obj.title}\"")
    db.add_citation(article_obj)

def edit_citation(db):
    """
    Asks for a citation and edits its details
    """
    cite_key = input("Enter the citation key of the citation to edit: ")
    citation_obj = db.get_one_citation(cite_key)
    if citation_obj is None:
        print("Citation not found.")
        return
    print("Leave the field blank to keep the current value.")
    new_title = input(f"Enter new title (current: {citation_obj.title}): ") or citation_obj.title
    new_author = input(
        f"Enter new author(s) (current: {citation_obj.author}): ") or citation_obj.author
    new_year = input(f"Enter new year (current: {citation_obj.year}): ") or citation_obj.year
    citation_obj.title = new_title
    citation_obj.author = new_author
    citation_obj.year = new_year
    print("Citation updated successfully.")

def add_tag(db):
    """
    Asks the user for a citation and the tags to add to it.
    """
    cite_key = input("Enter the citation key: ")
    citation_obj = db.get_one_citation(cite_key)
    if citation_obj is None:
        print("Citation not found.")
        return
    tags = input("Enter the tags: ").split(",")
    for tag in tags:
        citation_obj.add_tag(tag.strip())

def list_citations(db):
    """Prints the list of citations in the database."""
    print("Article Information:")
    # Listaa viitteet tietokannasta simpplisiti, jotta tägit voidaan liittää helpommin
    # lyhenne, otsikko, vuosi, tagit
    print_citation_list(db)

def save_to_file(db, default):
    """
    Asks the user to provide a file to save to.
    """
    filename = input("Enter the filename: ")
    if filename == "":
        filename = default
    db.save_to_file(f"data/{filename}.txt")

def load_from_file(db):
    """
    Asks the user to provide a file to load from.
    """
    filename= input("Enter the filename: ")
    if filename == "":
        print("No filename entered.")
        return
    db.load_from_file(f"data/{filename}")

def save_as_bibtex(db, default):
    """
    Asks the user to provide a bibtex file to save to.
    """
    filename = input("Enter the filename: ")
    if filename == "":
        filename = default
    db.save_as_bibtex(f"data/{filename}.bib")

def load_from_bibtex(db, default):
    """
    Asks the user to provide a bibtex file to load from
    """
    filename = input("Enter the filename: ")
    if filename == "":
        filename = default
    db.load_from_bibtex(f"data/{filename}.bib")

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
    for citation_obj in db.get_citations():
        # Needs to be in this format for the tests to work. Otherwise comparing object to string.
        print(str(citation_obj))
