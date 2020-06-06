from flask import jsonify
from typing import Dict, Union, List

from app import app
from .scraper import SCRAPERS


def get_articles(data: Dict[str, Union[str, int]]) -> Dict[str, str]:
    scraper = SCRAPERS[data['website']]()
    articles = scraper.get_articles(data['categories'],
                                    data['number'])
    return articles


@app.route('/website=<website>/category=<category>')
@app.route('/website=<website>/category=<category>/number=<int:number>')
@app.route('/website=<website>/category=<category>/date_range=<date_range>')
@app.route('/website=<website>/category=<category>/number=<int:number>/date_range=<date_range>')
def get_query(website: str, category: str, number: int = 3):

    data = {'website': website,
            'categories': category.split(','),
            'number': number}

    articles = get_articles(data)

    return jsonify(articles)


@app.errorhandler(404)
def not_found(arg):
    return jsonify({'error': 'url not found'}), 404
