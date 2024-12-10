""" Database module for storing citations """
import json
import article

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
        """Save citations to a file in JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump([citation.to_dict() for citation in self.citations], file, indent=4)
            print(f"Citations saved to {filename}")
        except IOError as e:
            print(f"Error saving to file: {e}")

    def load_from_file(self, filename: str):
        """Load citations from a file in JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                citations_data = json.load(file)
                self.citations = []
                for data in citations_data:
                    if 'journal' in data:
                        citation = article.Article(data['author'], data['title'],
                                                   data['journal'], data['year'])
                    else:
                        citation = citation.Citation(data['title'], data['author'], data['year'])
                    citation.tags = data.get('tags', [])
                    self.citations.append(citation)
        except FileNotFoundError:
            print("File not found")
        except IOError as e:
            print(f"Error loading from file {e}")
