from pathlib import Path

import scrapy


class NationalLibMedSpider(scrapy.Spider):
    name = "pmc"

    start_urls = ["https://www.ncbi.nlm.nih.gov/pmc/?term=kcnq5"]

    def parse(self, response):
        articles = response.css("div.rprt")
        for article in articles:
            yield {
                "title": article.css("div.title a").xpath("string()").get(),
                "authors": article.css("div.desc::text").get()
            }
