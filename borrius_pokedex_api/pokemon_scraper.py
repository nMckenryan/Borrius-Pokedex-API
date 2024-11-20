import datetime
from pathlib import Path

import scrapy
from scrapy.crawler import CrawlerProcess

class BorriusPokedexHelpers:
    def __init__(self):
        self.national_numbers = [246, 247, 248, 374, 375, 376, 443, 444, 445]
        self.borrius_numbers = range(1, 495)
        self.national_page = "https://www.pokemonunboundpokedex.com/national/"
        self.borrius_page = "https://www.pokemonunboundpokedex.com/borrius/"
        self.json_header = [
            {
                "info": {
                    "description": "Data pulled from BorriusPokedexScraper. https://github.com/nMckenryan/BorriusPokedexScraper",
                    "dataPulledOn": str(datetime.datetime.now()),
                },
                "pokemon": [],
            }
        ]
bph = BorriusPokedexHelpers()



class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

process = CrawlerProcess(
    settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    }
)

process.crawl(QuotesSpider)
process.start()  # the script will block here until the crawling is finished