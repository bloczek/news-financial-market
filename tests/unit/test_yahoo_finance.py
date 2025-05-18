import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from src.webscrapping_modules.yahoo_finance.yahoo_news import YahooMarketsScraper

class DummyBaseScraper:
    def __init__(self, base_url, headers):
        pass

@pytest.fixture(autouse=True)
def patch_basescraper(monkeypatch):
    monkeypatch.setattr(
        "src.webscrapping_modules.yahoo_finance.yahoo_news.BaseScraper",
        DummyBaseScraper
    )
    monkeypatch.setattr(
        "src.abstract.base.BaseScraper",
        DummyBaseScraper
    )

def test_parse_page_valid(monkeypatch):
    html = """
    <div class="carousel-top">
        <h3 class="header">US Markets</h3>
        <div class="tableContainer yf-t8m8uk">
            <table>
                <tr><td>APPL</td><td>Apple Inc.</td><td>150</td><td>+1.5</td></tr>
                <tr><td>GOOG</td><td>Alphabet</td><td>2800</td><td>-10</td></tr>
            </table>
        </div>
    </div>
    """
    scraper = YahooMarketsScraper()
    with patch("src.webscrapping_modules.yahoo_finance.yahoo_news.tabulate") as mock_tabulate:
        mock_tabulate.return_value = "table"
        with patch("builtins.print") as mock_print:
            scraper.parse_page(html)
            # Should print region, separator, table, and newline
            assert any("US Markets" in str(call) for call in mock_print.call_args_list)
            assert mock_tabulate.called

def test_parse_page_no_carousel_top():
    html = "<div></div>"
    scraper = YahooMarketsScraper()
    with pytest.raises(ValueError, match="No div with class 'carousel-top' found."):
        scraper.parse_page(html)

def test_parse_page_no_table_container():
    html = """
    <div class="carousel-top">
        <h3 class="header">Europe</h3>
    </div>
    """
    scraper = YahooMarketsScraper()
    with patch("builtins.print"):
        with pytest.raises(ValueError, match="No table container found for this header."):
            scraper.parse_page(html)

def test_parse_page_no_table():
    html = """
    <div class="carousel-top">
        <h3 class="header">Asia</h3>
        <div class="tableContainer yf-t8m8uk"></div>
    </div>
    """
    scraper = YahooMarketsScraper()
    with patch("builtins.print"):
        with pytest.raises(ValueError, match="No table found inside the table container."):
            scraper.parse_page(html)

def test_extract_and_display_table_with_data():
    html = """
    <table>
        <tr><td>TSLA</td><td>Tesla</td><td>700</td><td>+5</td></tr>
        <tr><td>MSFT</td><td>Microsoft</td><td>300</td><td>-2</td></tr>
    </table>
    """
    table = BeautifulSoup(html, "html.parser").find("table")
    scraper = YahooMarketsScraper()
    with patch("src.webscrapping_modules.yahoo_finance.yahoo_news.tabulate") as mock_tabulate:
        mock_tabulate.return_value = "table"
        with patch("builtins.print") as mock_print:
            scraper._extract_and_display_table(table)
            assert mock_tabulate.called
            assert mock_print.call_count >= 1

def test_extract_and_display_table_no_data():
    html = "<table></table>"
    table = BeautifulSoup(html, "html.parser").find("table")
    scraper = YahooMarketsScraper()
    with patch("builtins.print") as mock_print:
        scraper._extract_and_display_table(table)
        assert any("No data found in the table." in str(call) for call in mock_print.call_args_list)