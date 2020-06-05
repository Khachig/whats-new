import requests
from bs4 import BeautifulSoup
from typing import List


class Scraper:
    """
    Abstract Scraper class that is a blueprint for specific publication Scraper
    classes.
    Since there are different publications and each website is set up
    differently, a separate Scraper class is required for each publication that
    inherits Scraper and overrides the get_articles method.

    === Private Attributes ===
    _Name:
        Name of the publication this scraper scrapes.
    _URL:
        Url of the website this scraper scrapes.
    _CTG:
        List of categories listed on the website of the publication.
    """

    _NAME: str
    _URL: str
    _CTG: List[str]

    def __init__(self, publication_name: str, base_url: str,
                 categories: List[str]):
        self._NAME = publication_name
        self._URL = base_url
        self._CTG = categories

    def __repr__(self):
        return {f'{self._NAME}': f'{self._URL}',
                'categories': self._CTG}

    def get_name(self):
        return self._NAME

    def get_url(self):
        return self._URL

    def get_categories(self):
        return self._CTG

    def construct_request_url(self, category):
        raise NotImplementedError

    def get_articles(self, category, num, date):
        raise NotImplementedError
