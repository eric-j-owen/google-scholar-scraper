from pathlib import Path

import scrapy


class NationalLibMedSpider(scrapy.Spider):
    name = "pubmed"
    start_urls = ["https://www.ncbi.nlm.nih.gov/pmc/?term=kcnq5"]
    base_url = 'https://www.ncbi.nlm.nih.gov'

    def parse(self, response):
        articles = response.css("div.rprt")
        for article in articles:
            yield {
                "title": article.css("div.title a").xpath("string()").get(),
                "authors": article.css("div.desc::text").get(),
                "href": f'{self.base_url}{article.css(".title a::attr(href)").get()}'
            }
# output file command
# scrapy crawl pmc -O articles.json
# scrapy crawl pmc -o articles.jsonl
