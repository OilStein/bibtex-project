""" Database module for storing citations """

import json
import article

class Citations:
    """ Class for storing citations """
    def __init__(self):
        self.citations = []

    def add_citation(self, citation):
        """ Add citation to database """
        self.citations.append(citation)

    def get_citations(self):
        """ Get all citations """
        return self.citations
    
    def save_to_file(self, filename):
        """Save citations to a file"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for citation in self.citations:
                    file.write(str(citation) + '\n')
            print(f"Citations saved to {filename}")
        except Exception as e:
            print(f"Error saving to file")
            
    def load_from_file(self, filename):
        """Load citations from a file"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                self.citations = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"File not found")
        except Exception as e:
            print(f"Error loading from file")

    def print_citations(self):
        """ Print citations """
        for citation in self.citations:
            print(citation)

    def __str__(self):
        # lyhenne, otsikko, vuosi, tagit
        return f""
