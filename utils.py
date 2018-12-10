# coding: utf8
from models import RepositoryNode
from tabulate import tabulate
import json
import os

def create_nodes(filename):
	#for each file on the reposiroty, create a RepositoryNode to represent it
	leaf_nodes_list = []
	with open(filename) as f:
		data = json.load(f)
		for i, item in enumerate(data):
			leaf_nodes_list.append(RepositoryNode('/'.join(item['path']), item['repository'], item['path'], item['_bytes'], item['lines'], item['filename'], item['file_extension']))
	return leaf_nodes_list


def create_node_paths(leaf_nodes_list):
	#using the files nodes, creates RepositoryNodes to represent the folders of the repository
	#return two dicts that represents the root nodes(repostitories) and the paths nodes (folders)
	repositories_dict = {}
	folder_nodes_dict = {}
	for node in leaf_nodes_list:
		if not node.repository in repositories_dict:
			repositories_dict[node.repository] = RepositoryNode(full_path=node.repository, repository=node.repository, filename=node.repository)
		for i, path in enumerate(node.paths[2:], 2):
			current_full_path = '/'.join(node.paths[:i+1])
			parent_path = '/'.join(node.paths[:i])
			if not current_full_path in folder_nodes_dict and not current_full_path in repositories_dict:
				#update parents to the nodes being accessible from roots
				if parent_path == node.repository:
					folder_nodes_dict[current_full_path] = RepositoryNode(full_path=current_full_path, repository=node.repository, filename=path, parent=repositories_dict[parent_path])
				else:	
					folder_nodes_dict[current_full_path] = RepositoryNode(full_path=current_full_path, repository=node.repository, filename=path, parent=folder_nodes_dict[parent_path])

		parent_path = '/'.join(node.paths)
		if parent_path == node.repository:
			node.parent = repositories_dict[parent_path]
		else:
			node.parent = folder_nodes_dict[parent_path]
	return repositories_dict, folder_nodes_dict


def percentage(part, whole):
	return int(100 * float(part)/float(whole))


def get_repository_infos_print_format(repository_detail):
	#format the infos of the repository to be printed
	tab_list = []
	for key in repository_detail.keys():
		if not key in ['lines_total', 'size_total']:
			repository_detail[key]['lines_percentage'] = percentage(repository_detail[key]['lines'], repository_detail['lines_total'])
			repository_detail[key]['size_percentage'] = percentage(repository_detail[key]['bytes'], repository_detail['size_total'])
			line_format = '%s (%s %%)' % (repository_detail[key]['lines'], repository_detail[key]['lines_percentage'])
			size_format = '%s (%s %%)' % (repository_detail[key]['bytes'], repository_detail[key]['size_percentage'])
			tab_list.append([key, line_format, size_format])
	headers=['Extensão', 'Linhas', 'Bytes']
	return tabulate(tab_list, headers)


def parse_repositories_txt(filename):
	basedir = os.path.abspath(os.path.dirname(__file__))
	file_path =  os.path.join(basedir, filename)
	repositories = [line.rstrip('\n') for line in open(file_path)]
	return repositories


def get_scraped_items_file():
	basedir = os.path.abspath(os.path.dirname(__file__))
	filename =  os.path.join(basedir, 'github', 'items.json')
	return filename


def get_repository_filename(repository_name):
	_filename = repository_name.replace("/", "_") +'.txt'
	basedir = os.path.abspath(os.path.dirname(__file__))
	repository_filename =  os.path.join(basedir, 'repositories', _filename)
	return repository_filename


def parse_items():
	filename =  get_scraped_items_file()
	leaf_nodes_list = create_nodes(filename)
	repositories_dict, folder_nodes_dict = create_node_paths(leaf_nodes_list)
	for root in repositories_dict.values():
		repository_detail = root.get_repo_infos()
		repository_filename = get_repository_filename(root.repository)
		with open(repository_filename, "w") as text_file:
			text_file.write(root.repository)
			text_file.write('\n')
			text_file.write(get_repository_infos_print_format(repository_detail))
			text_file.write('\n')
			text_file.write(root.print_repository_tree())