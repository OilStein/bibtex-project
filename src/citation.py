""" Super class for all citation objects. """

class Citation:
    """Class for citation object"""
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"{self.author} ({self.year}). {self.title}."
