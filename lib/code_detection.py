import vim
import ast
import string
from os import path, walk

class CodeComparer:

  def __init__(self, codebase_path):
    self.code_paths_store = CodePathsStore(codebase_path)

  def compare(self, code):
    paths = ASTPath.get_paths(code)
    p = 0
    matches = {}
    for treepath in paths:

      match_files = None
      for path_dic in self.code_paths_store.paths:
        p += 1
        if treepath in path_dic["path"]:#.endswith(treepath):
          match_files = path_dic["files"]
          break

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

codebase_path = vim.eval("a:directory")
comparer = CodeComparer(codebase_path)
code = string.join(vim.current.buffer, "\n")
matches = comparer.compare(code)

for filename, match_percentage in matches.items():
    print filename, " {0:.2f}".format(match_percentage)
