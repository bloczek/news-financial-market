from bs4 import BeautifulSoup
from abstract.base import BaseScraper
from tabulate import tabulate

class YahooNewsScraper(BaseScraper):
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


class YahooMarketsScraper(BaseScraper):
    """
    A web scraper for extracting market data from Yahoo Finance.

    This scraper fetches the HTML content of the Yahoo Finance markets page and parses it
    to extract market data.
    """
    def __init__(self, base_url="https://finance.yahoo.com/markets/", headers=None):
        super().__init__(base_url, headers)

    def parse_page(self, html):
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find("div", class_="carousel-top")
        if not div:
            print("No div with class 'carousel-top' found.")
            raise ValueError("No div with class 'carousel-top' found.")

        h3_elements = div.find_all("h3", class_="header")
        for h3 in h3_elements:
            self._process_header_and_table(h3)

    def _process_header_and_table(self, h3):
        """
        Processes a single header and its associated table.
        """
        print(f"Region: {h3.text.strip()}")
        print("-" * 40)

        table_container = h3.find_next("div", class_="tableContainer yf-t8m8uk")
        if not table_container:
            print("No table container found for this header.")
            raise ValueError("No table container found for this header.")

        table = table_container.find("table")
        if not table:
            print("No table found inside the table container.")
            raise ValueError("No table found inside the table container.")

        self._extract_and_display_table(table)

    def _extract_and_display_table(self, table):
        """
        Extracts and displays the content of a table.
        """
        table_data = []
        for row in table.find_all("tr"):
            cells = [cell.text.strip() for cell in row.find_all("td")]
            if cells:  # Only add rows with data
                filtered_cells = cells[:1] + cells[2:]  # Remove the second column
                table_data.append(filtered_cells)

        if table_data:
            headers = ["Symbol", "Price", "Change"]  # Define table headers
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            print("\n")
        else:
            print("No data found in the table.")
            print("=" * 40)