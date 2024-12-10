""" Database module for storing citations """
from article import Article
import json

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
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for citation in self.citations:
                    citation_dict = {
                        "cite_key": citation.cite_key,
                        "title": citation.title,
                        "author": citation.author,
                        "journal": getattr(citation, "journal", ""),
                        "year": citation.year,
                        "tags": citation.tags
                    }
                    file.write(json.dumps(citation_dict) + '\n')
            print(f"Citations saved to {filename}")
        except IOError as e:
            print(f"Error saving to file: {e}")

    def load_from_file(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                self.citations = []
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        citation_dict = json.loads(line)
                        article = Article(
                            citation_dict["author"],
                            citation_dict["title"],
                            citation_dict["journal"],
                            citation_dict["year"]
                        )
                        article.tags = citation_dict["tags"]
                        self.citations.append(article)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}. Skipping line: {line}")
            print(f"Citations loaded from {filename}")
        except FileNotFoundError:
            print("File not found")
        except IOError as e:
            print(f"Error loading from file {e}")