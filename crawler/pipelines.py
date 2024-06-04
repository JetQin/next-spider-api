import asyncio
import logging
from itemadapter import ItemAdapter
from domain.book import Book

logger = logging.getLogger(__name__)


async def save_book(book: Book):
    await book.save()


class BookPipeline(object):
    db_conn = None

    def open_spider(self, spider):
        logger.info("open spider to start process crawler items")

    async def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        text = adapter.get("text")
        author = adapter.get("author")
        tags = adapter.get("tags", [])

        book = Book(text=text, author=author, tag=",".join(tags))
        logger.info("save book: %s, %s, %s", author, text, ','.join(tags))
        asyncio.run(save_book(book=book))
        return item

    def close_spider(self, spider):
        logger.info("close spider to finish process crawler items")