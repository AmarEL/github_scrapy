from anytree import NodeMixin, RenderTree


class RepositoryNode(NodeMixin):
	#A class that helps build a tree visualization of the repository/paths structure
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
		#compute the amount of lines and size for each extension
		if self.is_root:
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
		#return a string with the repository/paths structure
		str_tree = ''
		if self.is_root:
			for pre, _, node in RenderTree(self):
				if node.is_leaf:
					treestr = u"\n%s%s (%s linhas)" % (pre, node.filename, node.lines)
				elif node.is_root:
					treestr = u"\n%s[Project %s]" % (pre, node.filename)
				else:
					treestr = u"\n%s[%s]" % (pre, node.filename)
				str_tree = str_tree + treestr.ljust(8)
		return str_tree