from scrapy import Spider, Request
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ProxySpider(Spider):
    name = "httpbin"
    custom_settings = {
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "proxy": {
                "server": f"http://scraperapi.country_code=de:{os.getenv(key='SCRAPER_API_KEY')}@proxy-server.scraperapi.com:8001",
                "username": "scraperapi",
                "password": os.getenv(key="SCRAPER_API_KEY"),
            },
        },
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 100000
    }

    def start_requests(self):
        yield Request(
            "http://httpbin.org/get",
            meta={"playwright": True},
        )

    def parse(self, response):
        print(response.text)