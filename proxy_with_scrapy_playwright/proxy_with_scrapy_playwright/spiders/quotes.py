import scrapy
from scrapy_playwright.page import PageMethod
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class ProxySpider(scrapy.Spider):
    name = 'quotes'
    custom_settings = {
        "FEED_EXPORT_ENCODING": "utf-8", # UTF-8 deals with all types of characters
        "RETRY_TIMES": 3, # Retry failed requests up to 3 times
        "AUTOTHROTTLE_ENABLED": False, # Disables the AutoThrottle extension (recommended to be used with proxy services)
        "RANDOMIZE_DOWNLOAD_DELAY": False, # Should not be used with proxy services. If enabled, Scrapy will wait a random amount of time (between 0.5 * DOWNLOAD_DELAY and 1.5 * DOWNLOAD_DELAY) while fetching requests from the same website
        "CONCURRENT_REQUESTS": 5, # The maximum number of concurrent (i.e. simultaneous) requests that will be performed by the Scrapy downloader
        "DOWNLOAD_TIMEOUT": 60, # Setting the timeout parameter to 60 seconds as per the ScraperAPI documentation
        "ROBOTSTXT_OBEY": False, # Don't obey the Robots.txt rules
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": True,
            "proxy": {
                "server": f"http://scraperapi.country_code=de:{os.getenv(key='SCRAPER_API_KEY')}@proxy-server.scraperapi.com:8001",
                "username": "scraperapi",
                "password": os.getenv(key="SCRAPER_API_KEY"),
            },
        }, # A parameter to specify whether or not we want to launch an actual browser while scraping
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 100000
    }
    
    def start_requests(self):
        yield scrapy.Request(
            url="http://quotes.toscrape.com/js/",
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.quote"), # Type one of restaurants
                ],
                 "playwright_context_kwargs": {
                    "ignore_https_errors": True,
                },
                "playwright_include_page": True,
            },
            callback=self.parse,
        )

    async def parse(self, response):
        listings = response.css("div.quote")
        for li in listings:
            yield {
                "author": li.xpath(".//small[@class='author']/text()").get()
            }
