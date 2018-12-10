# coding: utf8
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from utils import parse_repositories_txt, parse_items
import sys

def craw(repositories):
	process = CrawlerProcess(get_project_settings())
	process.crawl('repositories', repositories=repositories)
	process.start()


if __name__ == "__main__":
	filename = sys.argv[1]
	repositories = parse_repositories_txt(filename)
	craw(repositories)
	parse_items()
