from scrapy import Spider, Request
import os
import re
from w3lib.html import remove_tags
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
        for i in range(0, 200):
            yield Request(
                "http://httpbin.org/user-agent",
                meta={"playwright": True, "playwright_include_page": True},
                callback=self.parse,
                dont_filter=True
            )

    async def parse(self, response):
        page = response.meta["playwright_page"] # The page object that allows us to interact with the webpage
        yield {"user-agent": re.findall(pattern="(?<=\"user-agent\": \")(.*)(?=\")", string=response.xpath("//pre/text()").get())[0]}
        await page.close()