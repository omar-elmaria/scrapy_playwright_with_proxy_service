from scrapy import Spider, Request
from scrapy.selector import Selector
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ProxySpider(Spider):
    name = "httpbin"
    custom_settings = {
        "FEED_EXPORT_ENCODING": "utf-8", # UTF-8 deals with all types of characters
        "CONCURRENT_REQUESTS": 20,
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
        for i in range(0, 4000):
            yield Request(
                "http://httpbin.org/user-agent",
                meta={"playwright": True, "playwright_include_page": True},
                callback=self.parse,
                errback=self.errback_close_page,
                dont_filter=True
            )

    async def parse(self, response):
        page = response.meta["playwright_page"] # The page object that allows us to interact with the webpage
        s  = Selector(text=await page.content())
        await page.close()
        yield {"user-agent": re.findall(pattern="(?<=\"user-agent\": \")(.*)(?=\")", string=s.xpath("//pre/text()").get())[0]}        
    
    async def errback_close_page(self, failure):
        page = failure.request.meta["playwright_page"]
        self.logger.warning("There was an error when processing %s: %s", failure.request, failure.value)
        await page.close()
