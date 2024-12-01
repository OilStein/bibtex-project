""" Database module for storing citations """

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
