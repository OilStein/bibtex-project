""" Super class for all citation objects. """

class Citation:
    """Class for citation object"""
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        self.tags = [""]
        self.cite_key = self.generate_cite_key()

    def add_tag(self, tag):
        """Add a tag to the citation"""
        # check if the tag is already in the list
        if tag in self.tags:
            return
        if self.tags[0] == "":
            self.tags = [tag]
        else:
            self.tags.append(tag)

    def generate_cite_key(self):
        """Generates a citation key for the article."""
        authors = self.author.split(" and") # BibTeX separates names with ' and'.
        surnames = ""
        for author in authors:
            surnames += author.split(' ')[-1]
        key = f"{surnames}{self.year}"
        return key

    def __str__(self):
        return f"{self.cite_key}, {self.title}, {self.author}, {self.year}, {self.tags}"
