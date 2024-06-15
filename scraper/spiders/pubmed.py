from pathlib import Path

import scrapy


class NationalLibMedSpider(scrapy.Spider):
    name = "pubmed"

    url = {
        "base": 'https://pubmed.ncbi.nlm.nih.gov',
        "search_term": "kcnq5",
        "page": 1,
    }

    start_urls = [
        f'{url["base"]}/?term={url["search_term"]}&page={url["page"]}'
    ]

    def parse(self, response):
        articles = response.css("div.docsum-content")
        if not articles:
            return
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
        self.page += 1
        next_url = f'{self.base_url}/?term={self.search_term}&page={self.page}'
        yield response.follow(next_url, self.parse)
# output file command
# scrapy crawl pmc -O articles.json
# scrapy crawl pmc -o articles.jsonl
