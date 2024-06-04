# -*- coding: utf-8 -*-
import logging

import scrapy
from crawler.model.book import BookItem
logger = logging.getLogger(__name__)


class BookSpider(scrapy.Spider):
    name = 'book'
    # start_urls = [
    #     'http://quotes.toscrape.com/',
    # ]

    async def parse(self,  response, **kwargs):
        self.logger.info("Parse function called on %s", response.url)
        for quote in response.xpath('//div[@class="quote"]'):
            text = quote.xpath('./span[@class="text"]/text()').extract_first(),
            author = quote.xpath('.//small[@class="author"]/text()').extract_first(),
            tags = quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            book = BookItem()
            book["text"] = text[0]
            book["author"] = author[0]
            book["tags"] = tags
            yield book
        self.crawler.stats.get_stats()
        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
