from webscrapping_modules.yahoo_news import YahooScraper

if __name__ == "__main__":
    scraper = YahooScraper()
    try:
        news_items = scraper.scrape()
        for item in news_items:
            print("Title:", item["title"])
            print("Link:", item["link"])
            print("-" * 40)
    except Exception as e:
        print(e)