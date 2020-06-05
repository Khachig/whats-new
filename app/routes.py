from flask import jsonify
from typing import Dict, Optional, Union

from app import app


def get_articles(data: Dict[str, Union[str, int]]) -> Dict[str, str]:
    articles = [{'article': 'https://example.com', 'image': 'https://image.com'} for i in range(data['number'])]
    return articles


@app.route('/website=<website>/category=<category>')
@app.route('/website=<website>/category=<category>/number=<int:number>')
@app.route('/website=<website>/category=<category>/date_range=<date_range>')
@app.route('/website=<website>/category=<category>/number=<int:number>/date_range=<date_range>')
def get_query(website: str, category: str, number: int = 3, date_range: Optional[str] = None):

    data = {'website': website,
            'category': category,
            'number': number,
            'date_range': date_range}

    articles = get_articles(data)

    return jsonify(articles)


@app.errorhandler(404)
def not_found(arg):
    return jsonify({'error': 'url not found'}), 404
