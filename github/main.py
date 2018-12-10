# coding: utf8
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from utils import create_nodes, create_node_paths, print_repository_infos


def craw():
	process = CrawlerProcess(get_project_settings())


	filename = '/home/amarel/vagas/github_scrapy/github/repositories.txt'
	repositories = [line.rstrip('\n') for line in open(filename)]
	
	# 'repositories' is the name of one of the spiders of the project.	
	process.crawl('repositories', repositories=repositories)
	process.start() # the script will block here until the crawling is finished


def process_items():
	filename = '/home/amarel/vagas/github_scrapy/github/github/items.json'
	leaf_nodes_list = create_nodes(filename)
	repositories_dict, folder_nodes_dict = create_node_paths(leaf_nodes_list)


	for root in repositories_dict.values():
		repository_detail = root.get_repo_infos()
		print(root.repository, '\n')
		print_repository_infos(repository_detail)
		root.print_repository_tree()

#craw()
process_items()