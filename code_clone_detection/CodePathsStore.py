#!/usr/bin/python

from os import path, walk
from .ASTPath import ASTPath
from .suffix_tree import SuffixTree
import pickle

class CodePathsStore:

  def __init__(self, codebase_path, file_extension):
    self.codebase_path = codebase_path
    self.file_extension = file_extension

    self.code_paths_filepath = path.join(codebase_path, ".cdp-" + self.file_extension + ".pkl")

    if not path.isfile(self.code_paths_filepath):
      self.make_code_paths_file()

    self.paths = self.get_code_paths_from_file()


  def make_code_paths_file(self):
    paths = {}
    for root, dirs, files in walk(self.codebase_path):
      for filename in files:
        if filename.endswith(self.file_extension):
          filename_path = path.join(root, filename)
          filepaths = ASTPath(filename_path, self.file_extension).paths
          string_paths = "".join(filepaths)
          paths[filename_path] = SuffixTree(string_paths)

    with open(self.code_paths_filepath, "wb") as code_paths_file:
      pickle.dump(paths, code_paths_file)


  def get_code_paths_from_file(self):
    paths = {}

    with open(self.code_paths_filepath, 'rb') as f:
      paths = pickle.load(f)

    return paths
