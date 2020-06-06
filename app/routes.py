import os
import json
from flask import jsonify, request, abort
from typing import Dict, Union

from app import app
from .scraper import SCRAPERS


def get_articles(data: Dict[str, Union[str, int]]) -> Dict[str, str]:
    scraper = SCRAPERS[data['website']]()
    articles = scraper.get_articles(data['categories'].split(','),
                                    data['number'])
    return articles


@app.route('/', methods=['GET'])
@app.route('/api', methods=['GET'])
def index():
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(basedir, 'index.json')
    with open(file_path, 'r') as json_file:
        json_data = json.loads(json_file.read())

    return jsonify(json_data)


@app.route('/api/get', methods=['GET'])
def get_query():

    args = request.args
    if 'website' not in args or 'categories' not in args:
        abort(400)

    articles = get_articles(args)

    return jsonify(articles)


@app.errorhandler(400)
def bad_request(arg):
    return jsonify({'error': 'bad request'})


@app.errorhandler(404)
def not_found(arg):
    return jsonify({'error': 'url not found'}), 404
