"""Tests for command_line.py"""
from unittest import TestCase, mock
from database import Citations
from article import Article
import command_line

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
    def test_start(self, mocked_input, mocked_print):
        """ This method tests the start method of the command_line module. """
        mocked_input.side_effect = [
            "new", "Sample Article", "John Doe",
              "Journal of Testing", "2023", "Java", "list", "print news report", "quit"]
        db = Citations()
        command_line.start(db)
        self.assertListEqual(
            mocked_print.mock_calls,
              [mock.call('Welcome to the citation database!'),
                mock.call('Commands: new, list, tag, save, load, quit, edit'),
                mock.call('Article Information:'),
                mock.call(
                    'Doe2023, Sample Article, John Doe, Journal of Testing, 2023, [\'Java\']'
                    ),
                mock.call('Invalid command. Please try again.')])

        self.assertListEqual(
            mocked_input.mock_calls, [
                mock.call("Enter a command: "),
                    mock.call("Enter the article title: "),
                    mock.call('Enter the author(s): '),
                    mock.call('Enter the journal name: '),
                    mock.call('Enter the publication year: '),
                    mock.call('Enter tags separated by commas: '),
                    mock.call('Enter a command: '),
                    mock.call('Enter a command: '),
                    mock.call('Enter a command: ')])

    @mock.patch("command_line.print", create=True)
    @mock.patch('command_line.input', create=True)
    def test_start_save(self, mocked_input, mocked_print):
        """ This method tests the start methods save of the command_line module. """
        mocked_input.side_effect = ["save", "xd", "quit"]
        db = Citations()
        art = Article("John Doe", "Sample Article", "Journal of Testing", "2023")
        art.add_tag("Java")
        art = Article("Jane Kimmel", "Another Article", "Journal of Testing", "2025")
        art.add_tag("Python")
        command_line.start(db)
        self.assertListEqual(
            mocked_print.mock_calls,
              [mock.call('Welcome to the citation database!'),
                mock.call('Commands: new, list, tag, save, load, quit, edit'),
                mock.call('Citations saved.'),
                mock.call('Invalid command. Please try again.')])

        self.assertListEqual(
            mocked_input.mock_calls, [
                mock.call("Enter a command: "),
                mock.call("Enter a command: "),
                mock.call("Enter a command: ")])

    @mock.patch("command_line.print", create=True)
    @mock.patch('command_line.input', create=True)
    def test_start_load(self, mocked_input, mocked_print):
        """ This method tests the start methods save of the command_line module. """
        mocked_input.side_effect = ["load", "quit"]
        db = Citations()
        command_line.start(db)
        self.assertListEqual(
            mocked_print.mock_calls,
              [mock.call('Welcome to the citation database!'),
                mock.call('Commands: new, list, tag, save, load, quit, edit'),
                mock.call('Citations loaded.'),
              ])


        self.assertListEqual(
            mocked_input.mock_calls, [
                mock.call("Enter a command: "),
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
                mock.call('Commands: new, list, tag, save, load, quit, edit'),
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
