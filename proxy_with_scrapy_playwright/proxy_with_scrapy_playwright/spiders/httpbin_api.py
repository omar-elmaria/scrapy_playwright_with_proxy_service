from scrapy import Spider, Request
import os
from dotenv import load_dotenv
from scraper_api import ScraperAPIClient

# Load environment variables
load_dotenv()

client = ScraperAPIClient(api_key=os.getenv(key="SCRAPER_API_KEY"))

class ProxyAPISpider(Spider):
    name = "httpbin_api"
    custom_settings = {
        "FEED_EXPORT_ENCODING": "utf-8", # UTF-8 deals with all types of characters
        "RETRY_TIMES": 3, # Retry failed requests up to 3 times
        "AUTOTHROTTLE_ENABLED": False, # Disables the AutoThrottle extension (recommended to be used with proxy services)
        "RANDOMIZE_DOWNLOAD_DELAY": False, # Should not be used with proxy services. If enabled, Scrapy will wait a random amount of time (between 0.5 * DOWNLOAD_DELAY and 1.5 * DOWNLOAD_DELAY) while fetching requests from the same website
        "CONCURRENT_REQUESTS": 20, # The maximum number of concurrent (i.e. simultaneous) requests that will be performed by the Scrapy downloader
        "DOWNLOAD_TIMEOUT": 60, # Setting the timeout parameter to 60 seconds as per the ScraperAPI documentation
        "ROBOTSTXT_OBEY": False, # Don't obey the Robots.txt rules
    }

    def start_requests(self):
        for i in range(0, 200):
            yield Request(
                client.scrapyGet(url="http://httpbin.org/get", country_code="de"),
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        print(response.text)    