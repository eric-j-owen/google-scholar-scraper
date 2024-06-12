from pathlib import Path

import scrapy


class NationalLibMedSpider(scrapy.Spider):
    name = "nlm"

    def start_requests(self):
        urls = ["https://www.ncbi.nlm.nih.gov/pmc/?term=kcnq5",
                "https://www.ncbi.nlm.nih.gov/pmc/?term=testing"
                ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        search_term = response.url.split("?")[-1]
        filename = f'nlm_{search_term}.html'
        Path(filename).write_bytes(response.body)
        self.log(f'saved file {filename}')
