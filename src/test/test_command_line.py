"""Tests for command_line.py"""
from test.test_citation import MockResponse
from unittest import TestCase, mock
from database import Citations
from article import Article
from citation import Citation
import command_line

WELCOME_MESSAGE_COUNT = 2
COMMANDS = [
        'new',
        'from doi',
        'list',
        'tag',
        'list by tag',
        'save',
        'load',
        'quit',
        'edit',
        'load bibtex',
        'save bibtex']
class TestCommandLine(TestCase):
    """ This class contains the tests for the command_line module. """

    @mock.patch('command_line.input', create=True)
    def test_get_article_info(self, mocked_input):
        """ This method tests the get_article_info method of the command_line module. """
        mocked_input.side_effect = ["Sample Article", "John Doe", "Journal of Testing", "2023", ""]
        result = command_line.get_article_info()
        self.assertEqual(str(result),
                          """Doe2023, Sample Article, John Doe, Journal of Testing, 2023, ['']""")

    @mock.patch("command_line.print", create=True)
    @mock.patch('command_line.input', create=True)
    def test_start_base_functionality(self, mocked_input, mocked_print):
        """Makes sure the start-method has basic functionality"""
        mocked_input.side_effect = ["quit"]
        db = Citations()
        command_line.start(db)
        self.assertListEqual(
            # Checking only first two for now
            mocked_print.mock_calls[:WELCOME_MESSAGE_COUNT],
            [
            mock.call('Welcome to the citation database!'),
            mock.call('Commands: ' + ', '.join(COMMANDS))
            ])
        # Check that we print correctly
        self.assertListEqual(mocked_input.mock_calls, [mock.call("Enter a command: ")])

    @mock.patch("command_line.print", create=True)
    @mock.patch('command_line.input', create=True)
    def test_start_commands_legal(self, mocked_input, mocked_print):
        """Makes sure start-method can handle illegal commands"""
        db = Citations()
        mocked_input.side_effect = ['', 'sorry', 'print', 'asdsf', 'quit']
        command_line.start(db)
        self.assertEqual(mocked_print.mock_calls[WELCOME_MESSAGE_COUNT:], \
                         [mock.call('Invalid command. Please try again.')] * 4)

    @mock.patch("command_line.print", create=True)
    @mock.patch('command_line.input', create=True)
    def test_start_new(self, mocked_input, mocked_print):
        """Makes sure start-method calls add_citation when new is given"""
        mocked_input.side_effect = ['new',
                                    'Sample Article',
                                    'John Doe',
                                    'Journal of Testing',
                                    '2023',
                                    'Python, Unit tests',
                                    "quit"]
        command_line.start(Citations())
        self.assertEqual(mocked_print.mock_calls[WELCOME_MESSAGE_COUNT:], [])
        self.assertEqual(mocked_input.mock_calls,
                         [mock.call("Enter a command: "),
                          mock.call("Enter the article title: "),
                          mock.call("Enter the author(s): "),
                          mock.call("Enter the journal name: "),
                          mock.call("Enter the publication year: "),
                          mock.call("Enter tags separated by commas: "),
                          mock.call("Enter a command: ")])

    @mock.patch("command_line.print", create=True)
    @mock.patch('command_line.input', create=True)
    def test_edit_citations_no_input(self, mocked_input, mocked_print):
        """This method tests editing citations with no input."""
        mocked_input.side_effect = ["Doe2023", "", "", ""]
        db = Citations()
        art = Article("John Doe", "Sample Article", "Journal of Testing", "2023")
        db.add_citation(art)
        command_line.edit_citation(db)
        self.assertEqual(str(db.get_one_citation("Doe2023")), str(art))
        self.assertEqual(mocked_print.mock_calls, [
            mock.call("Leave the field blank to keep the current value."),
            mock.call("Citation updated successfully.")])
        self.assertEqual(mocked_input.mock_calls, [
            mock.call("Enter the citation key of the citation to edit: "),
            mock.call("Enter new title (current: Sample Article): "),
            mock.call("Enter new author(s) (current: John Doe): "),
            mock.call("Enter new year (current: 2023): ")])

    @mock.patch("command_line.print", create=True)
    @mock.patch('command_line.input', create=True)
    def test_edit_citations_with_invalid_code(self, mocked_input, mocked_print):
        """This method tests editing citations with invalid ID."""
        mocked_input.side_effect = ["Joe2023"]
        db = Citations()
        art = Article("John Doe", "Sample Article", "Journal of Testing", "2023")
        db.add_citation(art)
        command_line.edit_citation(db)
        self.assertEqual(str(db.get_one_citation("Doe2023")), str(art))
        self.assertEqual(mocked_print.mock_calls, [mock.call("Citation not found.")])
        self.assertEqual(mocked_input.mock_calls, [
            mock.call("Enter the citation key of the citation to edit: ")])

    @mock.patch("command_line.print", create=True)
    @mock.patch('command_line.input', create=True)
    def test_edit_citations_with_changes(self, mocked_input, mocked_print):
        """This method tests editing citations with changes."""
        mocked_input.side_effect = ["Doe2023", "New Title", "", "2024"]
        db = Citations()
        art = Article("John Doe", "Sample Article", "Journal of Testing", "2023")
        db.add_citation(art)
        command_line.edit_citation(db)
        print(db.get_citations()[0])
        self.assertEqual(str(db.get_one_citation("Doe2023")), \
                         "Doe2023, New Title, John Doe, Journal of Testing, 2024, ['']")
        self.assertEqual(mocked_print.mock_calls, [
            mock.call("Leave the field blank to keep the current value."),
            mock.call("Citation updated successfully.")])
        self.assertEqual(mocked_input.mock_calls, [
            mock.call("Enter the citation key of the citation to edit: "),
            mock.call("Enter new title (current: Sample Article): "),
            mock.call("Enter new author(s) (current: John Doe): "),
            mock.call("Enter new year (current: 2023): ")])

    @mock.patch("command_line.print", create=True)
    @mock.patch('command_line.input', create=True)
    def test_save_to_file_with_no_input(self, mocked_input, mocked_print):
        """ Test that save_to_file can be called with empty string as filename """
        mocked_input.side_effect = [""]
        with mock.patch('database.Citations') as mock_citations:
            db = mock_citations.return_value
            art = Article("John Doe", "Sample Article", "Journal of Testing", "2023")
            art.add_tag("Java")
            db.add_citation(art)
            art = Article("Jane Kimmel", "Another Article", "Journal of Testing", "2025")
            art.add_tag("Python")
            db.add_citation(art)
            command_line.save_to_file(db, 'testi')

            # Check that the save_to_file method was called
            db.save_to_file.assert_called_once_with("data/testi.txt")
            self.assertListEqual(mocked_print.mock_calls, [])
            # Only asks for file
            self.assertListEqual(mocked_input.mock_calls, [mock.call("Enter the filename: ")])

    @mock.patch("command_line.print", create=True)
    @mock.patch('command_line.input', create=True)
    def test_save_to_file_with_input(self, mocked_input, mocked_print):
        """ This method tests the save_to_file method of the command_line module. """
        mocked_input.side_effect = ["somefile"]
        with mock.patch('database.Citations') as mock_citations:
            db = mock_citations.return_value
            art = Article("John Doe", "Sample Article", "Journal of Testing", "2023")
            art.add_tag("Java")
            db.add_citation(art)
            art = Article("Jane Kimmel", "Another Article", "Journal of Testing", "2025")
            art.add_tag("Python")
            db.add_citation(art)
            command_line.save_to_file(db, 'testi')

            # Check that the save_to_file method was called
            db.save_to_file.assert_called_once_with("data/somefile.txt")
            self.assertEqual(mocked_print.mock_calls, [])
            # Only asks for file
            self.assertEqual(mocked_input.mock_calls, [mock.call("Enter the filename: ")])

    @mock.patch('command_line.input', create=True)
    def test_start_load(self, mocked_input):
        """ This method tests the start methods save of the command_line module. """
        mocked_input.side_effect = ["load","dummy_data", "quit"]
        db = Citations()
        command_line.start(db)

        self.assertIn(mock.call('Enter the filename: '), mocked_input.mock_calls)



    @mock.patch("command_line.print", create=True)
    @mock.patch('command_line.input', create=True)
    def test_start_tag(self, mocked_input, mocked_print):
        """ This method tests the start methods tag of the command_line module. """
        mocked_input.side_effect = ["tag", "Doe2023", "Python", "tag", "xd", "quit"]
        db = Citations()
        art = Article("John Doe", "Sample Article", "Journal of Testing", "2023")
        art.add_tag("Java")
        db.add_citation(art)
        command_line.start(db)
        self.assertIn(mock.call('Citation not found.'), mocked_print.mock_calls)

        self.assertIn(mock.call('Enter the citation key: '), mocked_input.mock_calls)
        self.assertIn(mock.call('Enter the tags: '), mocked_input.mock_calls)

    @mock.patch("command_line.print", create=True)
    @mock.patch('command_line.input', create=True)
    def test_edit_article_no_changes(self, mocked_input, mocked_print):
        """This method tests the editing functionality of the command_line module."""
        mocked_input.side_effect = ["edit",
                                    "RidgewellCaldwell2013",
                                    "",
                                    "",
                                    "",
                                    "quit"]

        db = Citations()
        articles = [
            Article("John Doe",
                    "Sample Article",
                    "Journal of Testing",
                    "2023"),
            Article("Thomas Ridgewell and Elliot Caldwell",
                    "Dynamic huffman coding",
                    "IEEE",
                    "2013"),
            Article("Donald E Knuth",
                    "Structured Programming with go to Statements",
                    "ACM Computing Surveys (CSUR)",
                    "1974")
        ]
        for article in articles:
            db.add_citation(article)
        command_line.start(db)

        self.assertIn(
            mock.call('Leave the field blank to keep the current value.'),
            mocked_print.mock_calls)

        self.assertIn(mock.call('Citation updated successfully.'), mocked_print.mock_calls)

        self.assertIn(
            mock.call('Enter the citation key of the citation to edit: '),
            mocked_input.mock_calls)

        self.assertIn(
            mock.call('Enter new title (current: Dynamic huffman coding): '),
            mocked_input.mock_calls)

        self.assertIn(
            mock.call('Enter new author(s) (current: Thomas Ridgewell and Elliot Caldwell): '),
            mocked_input.mock_calls)

        self.assertIn(mock.call('Enter new year (current: 2013): '), mocked_input.mock_calls)


        changed_article = db.get_one_citation("RidgewellCaldwell2013")
        self.assertEqual(str(changed_article), str(articles[1]))

    @mock.patch("command_line.print", create=True)
    @mock.patch('command_line.input', create=True)
    def test_edit_article_editing_missing_citation(self, mocked_input, mocked_print):
        """This method tests that you can't edit citations that don't exist"""
        mocked_input.side_effect = ["edit",
                                    "Foo1111",
                                    "quit"]

        db = Citations()
        articles = [
            Article("John Doe",
                    "Sample Article",
                    "Journal of Testing",
                    "2023"),
            Article("Thomas Ridgewell and Elliot Caldwell",
                    "Dynamic huffman coding",
                    "IEEE",
                    "2013"),
            Article("Donald E Knuth",
                    "Structured Programming with go to Statements",
                    "ACM Computing Surveys (CSUR)",
                    "1974")
        ]
        for article in articles:
            db.add_citation(article)
        command_line.start(db)

        self.assertIn(mock.call('Citation not found.'), mocked_print.mock_calls)


    @mock.patch('command_line.input', create=True)
    def test_edit_article_changes_content(self, mocked_input):
        """This method tests that edits actually work"""
        mocked_input.side_effect = ["edit",
                                    "Doe2023",
                                    "Changed Title",
                                    "Jane Doe",
                                    "2023",
                                    "quit"]

        db = Citations()
        articles = [
            Article("John Doe",
                    "Sample Article",
                    "Journal of Testing",
                    "2023"),
            Article("Thomas Ridgewell and Elliot Caldwell",
                    "Dynamic huffman coding",
                    "IEEE",
                    "2013"),
            Article("Donald E Knuth",
                    "Structured Programming with go to Statements",
                    "ACM Computing Surveys (CSUR)",
                    "1974")
        ]
        for article in articles:
            db.add_citation(article)
        command_line.start(db)

        edited_article = db.get_one_citation('Doe2023')
        self.assertEqual(str(edited_article),
                         "Doe2023, Changed Title, Jane Doe, Journal of Testing, 2023, ['']")


    @mock.patch('requests.post', create=True)
    @mock.patch('command_line.input', create=True)
    def test_from_doi(self, mocked_input, mocked_post):
        """Test for testing from doi ui"""

        mocked_post.side_effect = [MockResponse()]

        mocked_input.side_effect = ["from doi", "10.5555/2387880.2387905", "quit"]

        db = Citations()

        command_line.start(db)

        self.assertEqual(str(db.get_citations()[0]),
        "C.JeffreyMichaelAndrewChristopherJ.SanjayAndreyChristopherPeterWilsonSebastianEugeneHongyiAlexanderSergeyDavidDavidSeanRajeshLindsayYasushiMichalChristopherRuthDale2012, Spanner: Google's globally-distributed database, Corbett, James C. and Dean, Jeffrey and Epstein, Michael and Fikes, Andrew and Frost, Christopher and Furman, J. J. and Ghemawat, Sanjay and Gubarev, Andrey and Heiser, Christopher and Hochschild, Peter and Hsieh, Wilson and Kanthak, Sebastian and Kogan, Eugene and Li, Hongyi and Lloyd, Alexander and Melnik, Sergey and Mwaura, David and Nagle, David and Quinlan, Sean and Rao, Rajesh and Rolig, Lindsay and Saito, Yasushi and Szymaniak, Michal and Taylor, Christopher and Wang, Ruth and Woodford, Dale, 2012, ['']") # pylint: disable=line-too-long

    @mock.patch('command_line.input', create=True)
    def test_load_from_bibtex(self, mocked_input):
        """Test for loading from .bib file"""
        # pylint: disable=duplicate-code
        mock_data = """@misc{Mikko2023,
	author = "Mikko",
	title = "Another Test",
	journal = "Testing Journal",
	year = "2023"
}""" # pylint: enable=duplicate-code
        mocked_input.side_effect = ["load bibtex", "test.bib", "quit"]
        db = Citations()
        with mock.patch("builtins.open", mock.mock_open(read_data=mock_data)):
            command_line.start(db)
        self.assertEqual(str(db.get_citations()[0]), "Mikko2023, Another Test, Mikko, 2023, ['']")

    @mock.patch('command_line.input', create=True)
    def test_save_as_bibtex(self, mocked_input):
        """Test for saving as a .bib file"""
        mocked_input.side_effect = ["save bibtex", "test.bib", "quit"]
        db = Citations()
        citation_obj = Citation("Another Test", "Mikko", 2023)
        db.add_citation(citation_obj)
        with mock.patch("builtins.open", mock.mock_open()) as mocked_file:
            command_line.start(db)
            self.assertIn(
                mock.call().write('@misc{Mikko2023,\n\tauthor = "Mikko",\n\ttitle = "Another Test",\n\tyear = "2023",\n\ttags = "[\'\']"\n}'), # pylint: disable=line-too-long
                mocked_file.mock_calls)
            self.assertIn(mock.call().write('\n\n'), mocked_file.mock_calls)
