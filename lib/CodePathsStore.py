#!/usr/bin/python

from os import path, walk
from .ASTPath import ASTPath

class CodePathsStore:

  def __init__(self, codebase_path):
    self.codebase_path = codebase_path

    self.code_paths_filepath = path.join(codebase_path, ".codeDetectPaths")

    if not path.isfile(self.code_paths_filepath):
      self.make_code_paths_file()

    self.paths = self.get_code_paths_from_file()


  def make_code_paths_file(self):
    paths = []
    for root, dirs, files in walk(self.codebase_path):
      for filename in files:
        if filename.endswith(".py"):
          filename_path = path.join(root, filename)
          filepaths = ASTPath(filename_path).paths
          for p in filepaths:
            ind = self.find_index_of_path(p, paths)
            if ind > -1:
              if filename_path not in paths[ind]["files"]:
                paths[ind]["files"].append(filename_path)
            else:
              paths.append({"path": p, "files": [filename_path]})


    with open(self.code_paths_filepath, "w") as code_paths_file:
      code_paths_file.writelines([treepath["path"] + " " + ",".join(treepath["files"]) + "\n" for treepath in paths])


  def get_code_paths_from_file(self):
    paths = []

    with open(self.code_paths_filepath) as code_paths_file:
      for line in code_paths_file:
        path_string, files_string = line.split()
        files = files_string.split(',')
        paths.append({"path": path_string, "files": files})

    return paths


  def find_index_of_path(self, treepath, paths=None):
    if paths is None:
      paths = self.paths
    return next((ind for (ind, dic) in enumerate(paths) if dic["path"] == treepath), -1)
