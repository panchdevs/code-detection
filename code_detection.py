import sublime, sublime_plugin, os
from .lib.CodeComparer import CodeComparer

class CodeDetectionCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.window().show_input_panel("Search directory", ".", self.compare, None, None)


  def compare(self, codebase_path):
    comparer = CodeComparer(codebase_path)
    code_body = self.view.substr(sublime.Region(0, self.view.size()))

    matches = comparer.compare(code_body)
    match_list = []
    for match in matches:
      for filename, match_percentage in match.items():
        match_list.append(filename + " {0:.2f}".format(match_percentage))
    self.view.window().show_quick_panel(match_list, self.something)


  def something(self):
    # added temporarily
    return ""