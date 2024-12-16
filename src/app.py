"""Main application file."""
import json

# pylint: disable=import-error
from flask import Flask, request
from flask_cors import CORS

from database import Citations


app = Flask(__name__)
CORS(app)
db = Citations()


@app.route('/a')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello, World!'

@app.route('/citations')
def get_all_citations():
    """Return JSON of citations."""
    response = app.response_class(
        response=json.dumps([citation.to_dict() for citation in db.get_citations()]),
        status=200,
        mimetype='application/json'
    )
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.post('/citations')
def post_citation():
    """Add a new citation."""
    data = request.get_json()
    if not data:
        return {"error": "Invalid input"}, 400

    try:
        db.add_citation(data)
        citation = db.get_one_citation(data['cite_key'])
        return json.dumps(citation.to_dict()), 201
    except KeyError as e:
        return {"error": str(e)}, 500




def init_app():
    """Initialize the app."""
    db.load_from_file('data/dd.txt')


def main():
    """Run the app."""
    init_app()
    app.debug = True
    app.run()

if __name__ == '__main__':
    main()
