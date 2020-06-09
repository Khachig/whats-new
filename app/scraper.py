import json
import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import Dict, List, Tuple, Union


class Scraper(ABC):
    """
    Abstract Scraper class that is a blueprint for specific publication Scraper
    classes.
    Since there are different publications and each website is set up
    differently, a separate Scraper subclass is required for each publication
    that overrides the get_articles and construct_request_url methods.

    === Static Attributes ===
    Name:
        Name of the publication this scraper scrapes.
    URL:
        Url of the website this scraper scrapes.
    CTG:
        List of categories listed on the website of the publication.
    """

    NAME: str
    URL: str
    CTG: List[str]

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def url(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def ctg(self):
        raise NotImplementedError

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError

    @abstractmethod
    def _send_request(self, category: str, num: int) -> List[dict]:
        raise NotImplementedError

    @abstractmethod
    def get_articles(self, category: str, num: int):
        raise NotImplementedError


class NarwhalScraper(Scraper):

    @property
    def name(self):
        return 'The Narwhal'

    @property
    def url(self):
        return 'www.thenarwhal.ca'

    @property
    def api(self):
        return 'wp-json/wp/v2'

    @property
    def ctg(self):
        categories = ['explainer', 'in-depth', 'investigation', 'news',
                      'newsletter', 'on-the-ground', 'opinion', 'photo-essay',
                      'profile', 'video']
        return categories

    def __repr__(self):
        return f'{self.name}: {self.url}\nCategories: {self.ctg}'

    def _get_ctg_dict(self) -> Dict[str, int]:
        ctg_ids = [6935, 6933, 6934, 6932, 7346, 7163, 6938, 6936, 7221, 6937]
        categories = {self.ctg[i]: ctg_ids[i] for i in range(len(ctg_ids))}
        return categories

    @staticmethod
    def _get_header_image(url: str) -> str:
        """
        Return a link to the banner image of the article given by <url>.
        """
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        banner = soup.find('section', class_='intro__banner')
        image = banner.find('div', class_='progressive')['data-href']
        return image

    def _get_author(self, author_id: int) -> Tuple[str, str]:
        """
        Return a tuple of two strings containing the name and link to profile
        page of the author given by <author_id>.
        """

        response = self._send_request('users', {'author_id': author_id})
        name = response['name']
        link = response['link']
        return name, link

    def _send_request(self, endpoint: str,
                      args: Dict[str, Union[str, int]]) -> \
            Union[List[dict], dict]:
        """
        Send GET request to The Narwhal api and return parsed json object.

        <endpoint> can be one of: users, posts
        """

        request_url = f'https://{self.url}/{self.api}/{endpoint}'
        if endpoint == 'posts':
            categories = self._get_ctg_dict()
            query_params = {'page': 1,
                            'categories': [categories[i] for i in args['categories']],
                            'per_page': args['number']
                            }
            response = requests.get(request_url, params=query_params)
        else:
            request_url += f'/{args["author_id"]}'
            response = requests.get(request_url)

        response_json = json.loads(response.content)
        return response_json

    @staticmethod
    def _html_p_to_text(html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.find('p').text
        return text

    def get_articles(self, data: Dict[str, str]) -> List[Dict[str, str]]:
        """
        Return a list of <num> elements, where each element is a dictionary
        containing the following metadata about the article:
            link: url link to the article
            headline: the headline of the article
            excerpt: a short excerpt from the article
            image: link to header image of the article
            date: date of publication
            author: name of author and link to their author page

        <categories> specifies what section of the website to search in.
        <num> specifies the number of articles to fetch.

        === Preconditions ===
        categories in self.ctg
        num >= 1
        """
        response = self._send_request('posts', data)
        articles = []
        for element in response:
            link = element['link']
            headline = element['title']['rendered']
            excerpt = self._html_p_to_text(element['excerpt']['rendered'])
            image = self._get_header_image(link)
            date = element['date']
            author_id = element['author']
            author_name, author_link = self._get_author(author_id)
            article = {'link': link,
                       'headline': headline,
                       'excerpt': excerpt,
                       'image': image,
                       'date': date,
                       'author': ','.join((author_name, author_link))}
            articles.append(article)

        return articles


SCRAPERS = {'the_narwhal': NarwhalScraper}
