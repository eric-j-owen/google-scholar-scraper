from pathlib import Path

import scrapy


class NationalLibMedSpider(scrapy.Spider):
    name = "pubmed"
    start_urls = ["https://pubmed.ncbi.nlm.nih.gov/?term=kcnq5"]
    base_url = 'https://pubmed.ncbi.nlm.nih.gov'

    def parse(self, response):
        articles = response.css("div.docsum-content")
        for article in articles:
            citation = {
                "short_authors": response.css(".short-authors::text").get(),
                "full_authors": response.css(".full-authors::text").get(),
                "journal": response.css(".short-journal-citation::text").get(),
                "pmid": response.css(".docsum-pmid::text").get(),
            }
            yield {
                "title": article.css("a").xpath("string()").get().replace('\n', '').strip(),
                "snippet": article.css(".short-view-snippet").xpath("string()").get().replace('\n', '').strip(),
                "citation": f'{citation["short_authors"]} {citation["journal"]} PMID: {citation["pmid"]}',
                "url": f'{self.base_url}{article.css("a::attr(href)").get()}'
            }
# output file command
# scrapy crawl pmc -O articles.json
# scrapy crawl pmc -o articles.jsonl
