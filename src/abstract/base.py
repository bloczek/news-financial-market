import requests
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    """
    An abstract base class for web scrapers. Provides methods for fetching web pages
    and defines an abstract method for parsing the content of a page.
    """
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36"
        }
    
    def get_page(self, url=None):
        """
        Fetches the HTML content of a web page.
        Args:
            url (str, optional): The URL of the page to fetch. If not provided, the base URL is used.
        Returns:
            str: The HTML content of the page.
        Raises:
            Exception: If the HTTP request fails or returns a non-200 status code.
        """
    
        if url is None:
            url = self.base_url
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            raise requests.exceptions.HTTPError(f"Error fetching {url}: {response.status_code}")
    
    @abstractmethod
    def parse_page(self, html):
        """
        Abstract method for parsing the content of a web page.
        Args:
            html (str): The HTML content of the page.
        Returns:
            Any: Parsed data from the page. The return type depends on the implementation.
        """
        pass
    
    def scrape(self, url=None):
        """
        Fetches and parses the content of a web page.
        Args:
            url (str, optional): The URL of the page to scrape. If not provided, the base URL is used.
        Returns:
            Any: Parsed data from the page. The return type depends on the implementation of `parse_page`.
        """
        html = self.get_page(url)
        return self.parse_page(html)