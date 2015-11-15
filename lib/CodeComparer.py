#!/usr/bin/python

from .ASTPath import ASTPath
from .CodePathsStore import CodePathsStore

class CodeComparer:

  def __init__(self, codebase_path):
    self.code_paths_store = CodePathsStore(codebase_path)

  def compare(self, code):
    paths = ASTPath.get_paths(code)

    matches = {}
    for treepath in paths:

      match_files = None
      for path_dic in self.code_paths_store.paths:
        if path_dic["path"].endswith(treepath):
          match_files = path_dic["files"]
          break

      if match_files is not None:
        for filename in match_files:
          if filename not in matches:
            matches[filename] = 1
          else:
            matches[filename] += 1

    number_of_paths = len(paths)

    match_percentages = []
    for filename, match_count in matches.items():
      match_percentage = (float(match_count) * 100) / number_of_paths
      match_percentages.append({filename: match_percentage})

    return match_percentages
