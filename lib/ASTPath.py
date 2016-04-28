#!/usr/bin/python

import ast
from .pycparser import c_parser

class ASTPath:

  def __init__(self, file_path, file_extension='.c'):
    self.file_path = file_path

    with open(file_path) as code_file:
      code_lines = code_file.readlines()

    code = "".join(code_lines)

    self.paths = self.get_paths(code, file_extension)

  @staticmethod
  def get_paths(code, file_extension):
    paths = []

    if file_extension == '.py':
        code_ast = ast.parse(code)
        ASTPath.build_paths_py(code_ast, paths, "")
    elif file_extension == '.c':
        parser = c_parser.CParser()
        code_ast = parser.parse(code, filename='<none>')
        ASTPath.build_paths_c(code_ast, paths, "")

    return paths

  @staticmethod
  def build_paths_py(node, paths, path_so_far):
    for field in ast.iter_fields(node):
      if(field[0] != 'body'):
        path_so_far += field[0]
        path_so_far += type(field[1]).__name__

    for child_node in ast.iter_child_nodes(node):
      ASTPath.build_paths_py(child_node, paths, path_so_far)

    if path_so_far:
      paths.append(path_so_far)

  @staticmethod
  def build_paths_c(node, paths, path_so_far):
    path_so_far += node.__class__.__name__

    for a in node.attr_names :
      if(getattr(node, a) and 'name' not in a and node.children()):
        path_so_far += str(getattr(node, a))
      
    for(child_name, child) in node.children() :
      ASTPath.build_paths_c(child, paths, path_so_far)

    if path_so_far:
     if path_so_far not in paths:
       path_so_far = path_so_far[7:]
       print(path_so_far)
       paths.append(path_so_far)

