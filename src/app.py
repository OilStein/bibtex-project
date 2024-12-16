"""Main application file."""

# pylint: disable=import-error
from flask import Flask
from flask_cors import CORS

from database import Citations
from routes import register_routes


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and methods
db = Citations()

register_routes(app, db)

def init_app():
    """Initialize the app."""
    db.load_from_file('data/citations.txt')


def main():
    """Run the app."""
    init_app()
    app.debug = True
    app.run()

if __name__ == '__main__':
    main()
