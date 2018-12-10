from anytree import NodeMixin, RenderTree
from tabulate import tabulate
import json

class RepositoryNode(NodeMixin):
	def __init__(self, full_path, repository, paths=None,  _bytes=None, lines=None, filename=None, file_extension=None, parent=None):
		self.full_path = full_path
		self.repository = repository
		self.paths = paths
		self._bytes = _bytes
		self.lines = lines
		self.filename = filename
		self.file_extension = file_extension[1:] if file_extension else file_extension #file_extension
		self.parent = parent


def create_node_paths():
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

def create_nodes(filename):
	with open(filename) as f:
		data = json.load(f)
		for i, item in enumerate(data):
			leaf_nodes_list.append(RepositoryNode('/'.join(item['path']), item['repository'], item['path'], item['_bytes'], item['lines'], item['filename'], item['file_extension']))


def percentage(part, whole):
  return int(100 * float(part)/float(whole))

def get_repo_infos(root):
	repository_detail = {}
	lines_total = 0
	size_total = 0
	for descendent in root.descendants:
		if descendent.is_leaf:
			lines_total += descendent.lines
			size_total += descendent._bytes
			if descendent.file_extension in repository_detail:
				repository_detail[descendent.file_extension]['lines'] += descendent.lines
				repository_detail[descendent.file_extension]['bytes'] += descendent._bytes
			else:
				repository_detail[descendent.file_extension] = {'lines': descendent.lines, 'bytes': descendent._bytes}

	tab_list = []
	for key in repository_detail.keys():
		repository_detail[key]['lines_percentage'] = percentage(repository_detail[key]['lines'], lines_total)
		repository_detail[key]['size_percentage'] = percentage(repository_detail[key]['bytes'], size_total)
		line_format = '%s (%s %%)' % (repository_detail[key]['lines'], repository_detail[key]['lines_percentage'])
		size_format = '%s (%s %%)' % (repository_detail[key]['bytes'], repository_detail[key]['size_percentage'])
		tab_list.append([key, line_format, size_format])
	
	headers=['Extensão', 'Linhas', 'Bytes']
	print(tabulate(tab_list, headers))



leaf_nodes_list = []
repositories_dict = {}
folder_nodes_dict = {}
filename = '/home/amarel/vagas/github_scrapy/github/github/items.json'
create_nodes(filename)
create_node_paths()


for root in repositories_dict.values():
	print(root.repository, '\n')
	get_repo_infos(root)
	for pre, _, node in RenderTree(root):
		if node.is_leaf:
			treestr = u"%s%s (%s linhas)" % (pre, node.filename, node.lines)
		else:
			treestr = u"%s%s" % (pre, node.filename)
		print(treestr.ljust(8))
