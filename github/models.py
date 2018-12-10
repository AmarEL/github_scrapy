from anytree import NodeMixin, RenderTree

class RepositoryNode(NodeMixin):
	def __init__(self, full_path, repository, paths=None,  _bytes=None, lines=None, filename=None, file_extension=None, parent=None):
		self.full_path = full_path
		self.repository = repository
		self.paths = paths
		self._bytes = _bytes
		self.lines = lines
		self.filename = filename
		self.file_extension = file_extension
		self.parent = parent


	def get_repo_infos(self):
		if self.is_root:
			print(self.repository, '\n')
			repository_detail = {'lines_total': 0, 'size_total': 0}
			for descendent in self.descendants:
				if descendent.is_leaf:
					repository_detail['lines_total'] += descendent.lines
					repository_detail['size_total'] += descendent._bytes
					if descendent.file_extension in repository_detail:
						repository_detail[descendent.file_extension]['lines'] += descendent.lines
						repository_detail[descendent.file_extension]['bytes'] += descendent._bytes
					else:
						repository_detail[descendent.file_extension] = {'lines': descendent.lines, 'bytes': descendent._bytes}
		return repository_detail


	def print_repository_tree(self):
		if self.is_root:
			for pre, _, node in RenderTree(self):
				if node.is_leaf:
					treestr = u"%s%s (%s linhas)" % (pre, node.filename, node.lines)
				else:
					treestr = u"%s%s" % (pre, node.filename)
				print(treestr.ljust(8))