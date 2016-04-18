#!/usr/bin/python

from .ASTPath import ASTPath
from .CodePathsStore import CodePathsStore

class CodeComparer:

  def __init__(self, codebase_path, file_extension):
    self.codebase_path = codebase_path
    self.file_extension = file_extension
    self.code_paths_store = CodePathsStore(codebase_path, self.file_extension)

  def compare(self, code):
    paths = ASTPath.get_paths(code, self.file_extension)

    matches = {}

    for treepath in paths:

      match_files = []
      for _filename, _suffixtree in self.code_paths_store.paths.items():
        if _suffixtree.find_substring(treepath) > -1:
          match_files.append(_filename)

      if match_files is not None:
        for filename in match_files:
          if filename not in matches:
            matches[filename] = 1
          else:
            matches[filename] += 1

    number_of_paths = len(paths)

    match_percentages = {}
    for filename, match_count in matches.items():
      match_percentage = (float(match_count) * 100) / number_of_paths
      match_percentages[filename] = match_percentage

    return match_percentages
