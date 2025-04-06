import requests
from bs4 import BeautifulSoup
from abstract.base import BaseScraper

class YahooScraper(BaseScraper):
    """
    A web scraper for extracting news articles from Yahoo Finance.

    This scraper fetches the HTML content of the Yahoo Finance news page and parses it
    to extract article titles and links.
    """
    def __init__(self, base_url="https://finance.yahoo.com/news/", headers=None):
        super().__init__(base_url, headers)
    
    def parse_page(self, html):
        """
        Parses the HTML content of the Yahoo Finance news page to extract article titles and links.
        Args:
            html (str): The HTML content of the page.
        Returns:
            list[dict]: A list of dictionaries, where each dictionary contains:
                - "title" (str): The title of the news article.
                - "link" (str): The URL of the news article.
        """
        soup = BeautifulSoup(html, "html.parser")
        items = []
        divs = soup.find_all("div", class_="content yf-82qtw3")
        
        for div in divs:
            a_tag = div.find("a", href=True)
            h3_tag = div.find("h3")
            
            if a_tag and h3_tag:
                title = h3_tag.text.strip()
                link = a_tag["href"]
                if not link.startswith("http"):
                    link = "https://finance.yahoo.com" + link
                items.append({"title": title, "link": link})
        return items
