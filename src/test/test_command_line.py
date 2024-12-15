"""Tests for command_line.py"""
from unittest import TestCase, mock
from database import Citations
from article import Article
import command_line

WELCOME_MESSAGE_COUNT = 2

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
        commands = [
            'new',
            'list',
            'tag',
            'save',
            'load',
            'quit',
            'edit',
            'load bibtex', 
            'save bibtex']
        db = Citations()
        mocked_input.side_effect = ["quit"]
        command_line.start(db)
        self.assertListEqual(
            # Checking only first two for now
            mocked_print.mock_calls[:WELCOME_MESSAGE_COUNT],
            [
            mock.call('Welcome to the citation database!'),
            mock.call('Commands: ' + ', '.join(commands))
            ])
        # Check that we print correctly
        self.assertEqual(mocked_input.mock_calls, [mock.call("Enter a command: ")])

    @mock.patch("command_line.print", create=True)
    @mock.patch('command_line.input', create=True)
    def test_save_to_file_with_input(self, mocked_input, mocked_print):
        """ This method tests the save_to_file method of the command_line module. """
        mocked_input.side_effect = ["testi"]
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
            self.assertEqual(mocked_print.mock_calls, [])
            # Only asks for file
            self.assertEqual(mocked_input.mock_calls, [mock.call("Enter the filename: ")])

    @mock.patch("command_line.print", create=True)
    @mock.patch('command_line.input', create=True)
    def test_start_load(self, mocked_input, mocked_print):
        """ This method tests the start methods save of the command_line module. """
        mocked_input.side_effect = ["load","dummy_data", "quit"]
        db = Citations()
        command_line.start(db)
        self.assertListEqual(
            mocked_print.mock_calls,
            [mock.call('Welcome to the citation database!'),
            mock.call('Commands: new, list, tag, save, load, quit, edit, load bibtex, save bibtex'),
            # mock.call('Citations loaded.'),
            ])


        self.assertListEqual(
            mocked_input.mock_calls, [
                mock.call("Enter a command: "),
                mock.call("Enter the filename: "),
                mock.call("Enter a command: "),
                ])


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
        self.assertListEqual(
            mocked_print.mock_calls,
            [mock.call('Welcome to the citation database!'),
            mock.call('Commands: new, list, tag, save, load, quit, edit, load bibtex, save bibtex'),
            mock.call('Citation not found.')
            ])

        self.assertListEqual(
            mocked_input.mock_calls, [
                mock.call("Enter a command: "),
                mock.call("Enter the citation key: "),
                mock.call("Enter the tags: "),
                mock.call("Enter a command: "),
                mock.call("Enter the citation key: "),
                mock.call("Enter a command: ")])

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

        self.assertListEqual(mocked_print.mock_calls, [
            mock.call('Welcome to the citation database!'),
            mock.call('Commands: new, list, tag, save, load, quit, edit, load bibtex, save bibtex'),
            mock.call('Leave the field blank to keep the current value.'),
            mock.call('Citation updated successfully.')])

        self.assertListEqual(mocked_input.mock_calls, [
            mock.call("Enter a command: "),
            mock.call('Enter the citation key of the citation to edit: '),
            mock.call('Enter new title (current: Dynamic huffman coding): '),
            mock.call('Enter new author(s) (current: Thomas Ridgewell and Elliot Caldwell): '),
            mock.call('Enter new year (current: 2013): '),
            mock.call('Enter a command: ')])

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

        self.assertListEqual(mocked_print.mock_calls, [
            mock.call('Welcome to the citation database!'),
            mock.call('Commands: new, list, tag, save, load, quit, edit, load bibtex, save bibtex'),
            mock.call('Citation not found.')])

        self.assertListEqual(mocked_input.mock_calls, [
            mock.call("Enter a command: "),
            mock.call('Enter the citation key of the citation to edit: '),
            mock.call('Enter a command: ')])

    @mock.patch("command_line.print", create=True)
    @mock.patch('command_line.input', create=True)
    def test_edit_article_changes_content(self, mocked_input, mocked_print):
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

        self.assertListEqual(mocked_print.mock_calls, [
            mock.call('Welcome to the citation database!'),
            mock.call('Commands: new, list, tag, save, load, quit, edit, load bibtex, save bibtex'),
            mock.call('Leave the field blank to keep the current value.'),
            mock.call('Citation updated successfully.')])

        self.assertListEqual(mocked_input.mock_calls, [
            mock.call('Enter a command: '),
            mock.call('Enter the citation key of the citation to edit: '),
            mock.call('Enter new title (current: Sample Article): '),
            mock.call('Enter new author(s) (current: John Doe): '),
            mock.call('Enter new year (current: 2023): '),
            mock.call('Enter a command: ')])

        edited_article = db.get_one_citation('Doe2023')
        self.assertEqual(str(edited_article),
                         "Doe2023, Changed Title, Jane Doe, Journal of Testing, 2023, ['']")
