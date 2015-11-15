#!/usr/bin/python

import ast

class ASTPath:

  def __init__(self, file_path):
    self.file_path = file_path

    with open(file_path) as code_file:
      code_lines = code_file.readlines()

    code = "".join(code_lines)

    self.paths = self.get_paths(code)

  @staticmethod
  def get_paths(code):
    code_ast = ast.parse(code)
    
    paths = []
    ASTPath.build_paths(code_ast, paths, "")

    return paths

  @staticmethod
  def build_paths(node, paths, path_so_far):
    for field in ast.iter_fields(node):
      if(field[0] != 'body'):
        path_so_far += field[0]
        path_so_far += type(field[1]).__name__

    for child_node in ast.iter_child_nodes(node):
      ASTPath.build_paths(child_node, paths, path_so_far)

    if path_so_far:
      paths.append(path_so_far)
