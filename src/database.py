""" Database module for storing citations """

class Citations:
    """ Class for storing citations """
    def __init__(self):
        self.citations = []

    def add_citation(self, citation: str):
        """ Add citation to database """
        self.citations.append(citation)

    def get_one_citation(self, cite_key: str):
        """ Get one citation by cite_key """
        for citation in self.citations:
            if citation.cite_key == cite_key:
                return citation
        return None

    def get_citations(self):
        """ Get all citations """
        return self.citations

    def save_to_file(self, filename: str):
        """Save citations to a file"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for citation in self.citations:
                    file.write(str(citation) + '\n')
            print(f"Citations saved to {filename}")
        except IOError as e:
            print(f"Error saving to file: {e}")

    def load_from_file(self, filename: str):
        """Load citations from a file"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                self.citations = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print("File not found")
        except IOError as e:
            print(f"Error loading from file {e}")

    def print_citations(self):
        """ Print citations """
        for citation in self.citations:
            print(citation)
