import re

""" Super class for all citation objects. """

class Citation:
    """Class for citation object"""
    def __init__(self, title, author, year, **kwargs):
        self.title = title
        self.author = author
        self.year = year
        self.tags = kwargs.get("tags", [""])
        self.cite_key = self.generate_cite_key()

    @classmethod
    def from_bib(cls, bibtex):
        data = Citation.parse_bibtex_entry(bibtex)
        return cls(**data)

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

    def print_as_bibtex(self):
        """Prints the article in BibTeX format."""
        return (
            f'@misc{{{self.cite_key},\n'
            f'\tauthor = "{self.author}",\n'
            f'\ttitle = "{self.title}",\n'
            f'\tyear = "{self.year}"\n'
            f'\ttags = "{self.tags}"\n'
            f'}}'
        )

    @classmethod
    def parse_bibtex_entry(cls, bibtex_str):
        # Define a regex pattern to match the BibTeX fields
        pattern = r'(?P<key>@article\{(?P<identifier>[^,]+),\s*(?P<fields>.+?)\s*\})'
        match = re.search(pattern, bibtex_str, re.DOTALL)

        if match:
            identifier = match.group('identifier')
            fields_str = match.group('fields')
            
            # Now we need to extract key-value pairs from the fields
            fields = {}
            for line in fields_str.split(','):
                key_value = line.split('=', 1)
                if len(key_value) == 2:
                    key = key_value[0].strip()
                    value = key_value[1].strip().strip('"').strip()
                    fields[key] = value
                    
            return {'identifier': identifier, **fields}

    def to_dict(self):
        """Convert to a dictionary"""
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "tags": self.tags,
            "cite_key": self.cite_key
        }

    def __str__(self):
        return f"{self.cite_key}, {self.title}, {self.author}, {self.year}, {self.tags}"


if __name__ == "__main__":
    bibtex_str = """@article{Doe2023,
        author = "John Doe",
        title = "Sample Article",
        journal = "Journal of Testing",
        year = "2023"
}"""
    obj = Citation.from_bib(bibtex_str)
    print(str(obj))
