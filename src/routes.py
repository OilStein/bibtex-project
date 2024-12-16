"""Routes for the Flask app."""
import json
from flask import request, send_file

from database import Citations
from article import Article

def register_routes(app, db):
    """Register routes."""
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
        print(data)
        if not data:
            return {"error": "Invalid input"}, 400
        try:
            title = data.get('title')
            author = data.get('author')
            year = data.get('year')
            journal = data.get('journal')
            tmp_citation = Article(author, title, journal, year)
            tmp_citation.tags = data.get('tags', [])
            tmp_citation.cite_key =tmp_citation.generate_cite_key()

            # print(str(tmp_citation))
            db.add_citation(tmp_citation)
            return tmp_citation.to_dict(), 201

        except KeyError as e:
            return {"error": str(e)}, 500

    @app.put('/citations/<cite_key>')
    def put_citation(cite_key):
        """Update a citation."""
        data = request.get_json()
        if not data:
            return {"error": "Invalid input"}, 400
        try:
            title = data.get('title')
            author = data.get('author')
            year = data.get('year')
            journal = data.get('journal')
            tmp_citation = Article(authors=author, journal=journal, year= year, title=title)
            tmp_citation.tags = data.get('tags', [])
            tmp_citation.cite_key = data.get('cite_key', tmp_citation.generate_cite_key())
            db.update_citation(cite_key, tmp_citation)

            return tmp_citation.to_dict(), 201
        except KeyError as e:
            return {"error": str(e)}, 404

    @app.delete('/citations/<cite_key>')
    def delete_citation(cite_key):
        """Delete a citation."""
        try:
            print(cite_key)
            tmp = db.get_one_citation(cite_key)
            db.delete_citation(cite_key)
            return tmp.to_dict(), 200
        except KeyError as e:
            return {"error": str(e)}, 404

    @app.post('/bibtex')
    def download_bibtex():
        """Takes list of cite_keys from JSON and returns a BibTeX file."""
        data = request.get_json()
        if not data or 'keys' not in data:
            return {"error": "Invalid input"}, 400
        try:
            cite_keys = data['keys']
            tmp_citations = Citations()
            for key in cite_keys:
                tmp_citations.add_citation(db.get_one_citation(key))
            tmp_citations.save_as_bibtex("data/dd.txt")
            return send_file("data/dd.txt", as_attachment=True, download_name="dd.txt"), 200
        except FileNotFoundError as e:
            return {"error": str(e)}, 404
