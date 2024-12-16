""" This module contains the tests for the Citation class. """
from unittest import TestCase, mock
from citation import Citation

class TestCitation(TestCase):
    """ This class contains the tests for the Citation class. """
    def test_from_bib(self):
        """Test creating a citation from bibtex"""
        data = """@misc{Mikko2023,
	author = "Mikko",
	title = "Another Test",
	year = "2023"
}"""
        citation_obj = Citation.from_bib(data)
        self.assertTrue(citation_obj.title == "Another Test")
        self.assertTrue(citation_obj.author == "Mikko")
        self.assertTrue(citation_obj.year == "2023")

    def test_print_as_bibtex(self):
        """Test printing a citation as bibtex"""
        citation_obj = Citation("Another Test", "Mikko", 2023)
        data = """@misc{Mikko2023,
	author = "Mikko",
	title = "Another Test",
	year = "2023",
	tags = "['']"
}"""
        self.assertEqual(data, citation_obj.print_as_bibtex())

    @mock.patch('requests.post', create=True)
    def test_from_doi(self, mocked_post):
        """Test creating a citation from doi"""
        class MockResponse(): # pylint: disable=too-few-public-methods
            """class for mocking a response"""
            def json(self):
                """method for mocking a response's json method"""
                return {'exportedDoiLength': 1,
                        'fileName': 'acm_2387880.2387905',
                        'suffix': 'bib',
                        'contentType': 'Application/x-bibtex',
                        'items': [{'10.5555/2387880.2387905':
                        {'id': '10.5555/2387880.2387905',
                         'type': 'PAPER_CONFERENCE',
                         'author': [
                            {'family': 'Corbett', 'given': 'James C.'},
                            {'family': 'Dean', 'given': 'Jeffrey'},
                            {'family': 'Epstein', 'given': 'Michael'},
                            {'family': 'Fikes', 'given': 'Andrew'},
                            {'family': 'Frost', 'given': 'Christopher'},
                            {'family': 'Furman', 'given': 'J. J.'},
                            {'family': 'Ghemawat', 'given': 'Sanjay'},
                            {'family': 'Gubarev', 'given': 'Andrey'},
                            {'family': 'Heiser', 'given': 'Christopher'},
                            {'family': 'Hochschild', 'given': 'Peter'},
                            {'family': 'Hsieh', 'given': 'Wilson'},
                            {'family': 'Kanthak', 'given': 'Sebastian'},
                            {'family': 'Kogan', 'given': 'Eugene'},
                            {'family': 'Li', 'given': 'Hongyi'},
                            {'family': 'Lloyd', 'given': 'Alexander'},
                            {'family': 'Melnik', 'given': 'Sergey'},
                            {'family': 'Mwaura', 'given': 'David'},
                            {'family': 'Nagle', 'given': 'David'},
                            {'family': 'Quinlan', 'given': 'Sean'},
                            {'family': 'Rao', 'given': 'Rajesh'},
                            {'family': 'Rolig', 'given': 'Lindsay'},
                            {'family': 'Saito', 'given': 'Yasushi'},
                            {'family': 'Szymaniak', 'given': 'Michal'},
                            {'family': 'Taylor', 'given': 'Christopher'},
                            {'family': 'Wang', 'given': 'Ruth'},
                            {'family': 'Woodford', 'given': 'Dale'}],
                         'accessed': {'date-parts': [[2024, 12, 16]]},
                         'issued': {'date-parts': [[2012, 10, 8]]},
                         'original-date': {'date-parts': [[2012, 10, 8]]},
                         'abstract': "Spanner is Google's scalable, multi-version, globally-distributed, and synchronously-replicated database. It is the first system to distribute data at global scale and support externally-consistent distributed transactions. This paper describes how Spanner is structured, its feature set, the rationale underlying various design decisions, and a novel time API that exposes clock uncertainty. This API and its implementation are critical to supporting external consistency and a variety of powerful features: nonblocking reads in the past, lock-free read-only transactions, and atomic schema changes, across all of Spanner.", # pylint: disable=line-too-long
                         'call-number': '10.5555/2387880.2387905',
                         'collection-title': "OSDI'12",
                         'container-title': 'Proceedings of the 10th USENIX conference on Operating Systems Design and Implementation', # pylint: disable=line-too-long
                         'event-place': 'Hollywood, CA, USA',
                         'ISBN': '9781931971966',
                         'number-of-pages': '14', 
                         'page': '251–264',
                         'publisher': 'USENIX Association',
                         'publisher-place': 'USA',
                         'title': "Spanner: Google's globally-distributed database"}}]}
        mocked_post.side_effect = [MockResponse()]

        citation_obj = Citation.from_doi("10.5555/2387880.2387905")

        self.assertEqual("Spanner: Google's globally-distributed database", citation_obj.title)

    @mock.patch("citation.print", create=True)
    @mock.patch('requests.post', create=True)
    def test_from_bad_doi(self, mocked_post, mocked_print):
        """Test failing in creating a citation from doi"""
        class MockResponse(): # pylint: disable=too-few-public-methods
            """class for mocking a response"""
            def json(self):
                """method for mocking a response's json method"""
                return {}

        mocked_post.side_effect = [MockResponse()]

        Citation.from_doi("10.5555/2387880.2387905")

        self.assertIn(mock.call("Received bad data"), mocked_print.mock_calls)

    def test_str(self):
        """Test for testing __str__ method"""
        citation_obj = Citation("Another Test", "Mikko", 2023)
        self.assertEqual("Mikko2023, Another Test, Mikko, 2023, ['']", str(citation_obj))
