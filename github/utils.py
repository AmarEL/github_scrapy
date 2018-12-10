# coding: utf8
from models import RepositoryNode
from tabulate import tabulate
import json


def create_nodes(filename):
	leaf_nodes_list = []
	with open(filename) as f:
		data = json.load(f)
		for i, item in enumerate(data):
			leaf_nodes_list.append(RepositoryNode('/'.join(item['path']), item['repository'], item['path'], item['_bytes'], item['lines'], item['filename'], item['file_extension']))
	return leaf_nodes_list


def create_node_paths(leaf_nodes_list):
	repositories_dict = {}
	folder_nodes_dict = {}
	for node in leaf_nodes_list:
		if not node.repository in repositories_dict:
			repositories_dict[node.repository] = RepositoryNode(full_path=node.repository, repository=node.repository, filename=node.repository)
		for i, path in enumerate(node.paths[2:], 2):
			current_full_path = '/'.join(node.paths[:i+1])
			parent_path = '/'.join(node.paths[:i])
			if not current_full_path in folder_nodes_dict and not current_full_path in repositories_dict:
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


def print_repository_infos(repository_detail):
	tab_list = []
	for key in repository_detail.keys():
		if not key in ['lines_total', 'size_total']:
			repository_detail[key]['lines_percentage'] = percentage(repository_detail[key]['lines'], repository_detail['lines_total'])
			repository_detail[key]['size_percentage'] = percentage(repository_detail[key]['bytes'], repository_detail['size_total'])
			line_format = '%s (%s %%)' % (repository_detail[key]['lines'], repository_detail[key]['lines_percentage'])
			size_format = '%s (%s %%)' % (repository_detail[key]['bytes'], repository_detail[key]['size_percentage'])
			tab_list.append([key, line_format, size_format])

	headers=['Extensão', 'Linhas', 'Bytes']
	print(tabulate(tab_list, headers), '\n')