import sublime, sublime_plugin, os
from .lib.CodeComparer import CodeComparer

class CodeDetectionCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    self.view.window().show_input_panel("Search directory", "", self.compare, None, None)


  def compare(self, codebase_path):
    comparer = CodeComparer(codebase_path)
    code_body = self.view.substr(sublime.Region(0, self.view.size()))

    matches = comparer.compare(code_body)
    match_list = []

    for filename, match_percentage in matches.items():
      match_list.append((filename, match_percentage))

    match_list.sort(key=lambda m: m[1], reverse=True)

    self.files = []
    panel_list = []

    for filename, match_percentage in match_list:
      panel_list.append(filename + " {0:.2f}".format(match_percentage))
      self.files.append(filename)

    self.view.window().show_quick_panel(panel_list, self.show_file)


  def show_file(self, index):
    if index > -1:
      self.view.window().open_file(self.files[index])