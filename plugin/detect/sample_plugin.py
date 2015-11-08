import sublime, sublime_plugin
import ast
import re
import sys
import os
class sampleCommand(sublime_plugin.TextCommand):
	


	def run(self, edit):
		body = self.view.substr(sublime.Region(0, self.view.size()))
		self.view.window().show_input_panel("Enter Directory Path: ", '', self.call, None, self.view.window())
	def call(self, dirname):
		self.view.window().run_command("show_panel")
		print(dirname)
		self.input_file = self.view.file_name()
		print(self.input_file)
		self.main_stuff(self.input_file, dirname)

	#l1 will store root to leaf  paths for complete code
	l1 = []
	#l2 will store root to leaf paths for incomplete code
	l2 = []
	#store filenames of complete codes and matching percentage to incomplete code														
	d = {}														
	
	def main_stuff(self, filename, dirname):
		self.build_incomplete_code_ast(filename)
		self.iterate_directory(dirname)
		print("Current File : ", filename)
		print("Filename : \tMatching Percentage ")
		for filename, match in self.d.items():
			print(filename," : ", "{0:.2f}".format(round(match,2)))


	
	def prettyprint(self, node, no_of_space, p, i):					#to create all root to leaf paths
		#print(" "*no_of_space,"Node: ", node)
		#if(no_of_space != 0):
		for f in ast.iter_fields(node):
			#print(" "*no_of_space, f)
			if(f[0] != 'body'):									#f is a tuple
				p += f[0] + " "									
				p += (type(f[1]).__name__ + " ")				#for storing node types, if node is 'op' (operator) then type.__name__ will give 'Add'
	
		for n in ast.iter_child_nodes(node):
			self.prettyprint(n, no_of_space+2, p, i)
	    
		else :
			if(i == 1):
				self.l1.append(p)
			else:
				self.l2.append(p)


	def extract_file_code(self, f):
		str = ""
		for line in f:
			str += line
		return str
	
	
	def build_incomplete_code_ast(self, file_name):
		f_incomplete = open(file_name)
		str_incomplete = ""
		str_incomplete = self.extract_file_code(f_incomplete)
		print(str_incomplete)
		tree_incomplete = ast.parse(str_incomplete)
		self.prettyprint(tree_incomplete, 0, "", 2)
	
	def iterate_directory(self, dir_name):
		for filename in os.listdir(dir_name):
			self.l1[:] = []
			
			f_complete = open(dir_name+'\\'+filename)					#change it to backslash for unix based systems
			str_complete = self.extract_file_code(f_complete)
			print(filename,":\n")
			print(filename)
			tree_complete = ast.parse(str_complete)
			self.prettyprint(tree_complete, 0, "", 1)
			self.match_paths(filename)
	


	def match_paths(self, filename):
		match = 0
		for w2 in self.l2:
			w2.strip()
			for w1 in self.l1:
				w1.strip()
				if(w2 in w1 and w2 != ' ') :
					match += 1
					#l1.remove(w1)
					break
	
		t = (float(match) * 100 ) / len(self.l2)
		self.d[filename] = t

