import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from fastapi import APIRouter, BackgroundTasks
from crawler.spiders.book_spider import BookSpider

router = APIRouter(tags=["spider"])


def create_task(domain: str):
    settings = get_project_settings()
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'crawler.settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    settings.setmodule(settings_module_path, priority='project')
    process = CrawlerProcess(settings=settings)
    process.crawl(BookSpider, start_urls=[domain])
    process.start()  # the script will block here until the crawling is finished


@router.post("/run_task")
async def run_task(domain: str, tasks: BackgroundTasks):
    tasks.add_task(create_task, domain)
    return {"msg": "success"}
