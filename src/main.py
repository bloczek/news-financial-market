from webscrapping_modules.yahoo_finance.yahoo_news import YahooNewsScraper, YahooMarketsScraper

if __name__ == "__main__":
    scraper_news = YahooNewsScraper()
    scraper_markets = YahooMarketsScraper()

    try:
        news_items = scraper_news.scrape()
        # Print the extracted news items
        for item in news_items:
            print("Title:", item["title"])
            print("Link:", item["link"])
            print("-" * 40)
            # initialize the YahooMarketsScraper
        scraper_markets.scrape()
    except Exception as e:
        print(e)