from scrapy import Spider, Request
import os
from dotenv import load_dotenv
from scraper_api import ScraperAPIClient

# Load environment variables
load_dotenv()

class ProxyAPISpider(Spider):
    name = "zyte_api"
    custom_settings = {
        "FEED_EXPORT_ENCODING": "utf-8", # UTF-8 deals with all types of characters
        "RETRY_TIMES": 3, # Retry failed requests up to 3 times
        "AUTOTHROTTLE_ENABLED": False, # Disables the AutoThrottle extension (recommended to be used with proxy services)
        "RANDOMIZE_DOWNLOAD_DELAY": False, # Should not be used with proxy services. If enabled, Scrapy will wait a random amount of time (between 0.5 * DOWNLOAD_DELAY and 1.5 * DOWNLOAD_DELAY) while fetching requests from the same website
        "CONCURRENT_REQUESTS": 20, # The maximum number of concurrent (i.e. simultaneous) requests that will be performed by the Scrapy downloader
        "DOWNLOAD_TIMEOUT": 60, # Setting the timeout parameter to 60 seconds as per the ScraperAPI documentation
        "ROBOTSTXT_OBEY": False, # Don't obey the Robots.txt rules
        # Zyte API settings
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
        },
        "REQUEST_FINGERPRINTER_CLASS": "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        "ZYTE_API_KEY": os.getenv(key="ZYTE_API_KEY"),
        "ZYTE_API_TRANSPARENT_MODE": True,
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
    }

    def start_requests(self):
        for i in range(1, 10):
            yield Request(
                url="http://httpbin.org/ip",
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        print(response.text)    