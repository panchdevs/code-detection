#!/usr/bin/python

from os import path, walk
from ASTPath import ASTPath

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
          filepaths = ASTPath(filename).paths
          for p in filepaths:
            ind = self.find_index_of_path(p, paths)
            if ind > -1:
              paths[ind]["files"].append(path.join(root, filename))
            else:
              paths.append({"path": p, "files": [path.join(root, filename)]})


    with open(self.code_paths_filepath, "w") as code_paths_file:
      code_paths_file.writelines([treepath["path"] + " " + ",".join(treepath["files"]) + "\n" for treepath in paths])


  def get_code_paths_from_file(self):
    paths = []

    with open(self.code_paths_filepath) as code_paths_file:
      for line in code_paths_file:
        path_string, files_string = line.split()
        files = files_string.split(',')
        paths.append({"path": path, "files": files})

    return paths


  def find_index_of_path(self, treepath, paths=None):
    if paths is None:
      paths = self.paths
    return next((ind for (ind, dic) in enumerate(paths) if dic["path"] == treepath), -1)


CodePathsStore(".")