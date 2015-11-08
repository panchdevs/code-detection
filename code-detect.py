import ast
import re
import sys
import os

l1 = []
l2 = []
d = {}

def prettyprint(node, no_of_space, p, i):
    #print(" "*no_of_space,"Node: ", node)
    #if(no_of_space != 0):
    for f in ast.iter_fields(node):
    	#print(" "*no_of_space, f)
    	if(f[0] != 'body'):
    		p += f[0] + " "
    		p += (type(f[1]).__name__ + " ")

    for n in ast.iter_child_nodes(node):
        prettyprint(n, no_of_space+2, p, i)
    
    else :
    	if(i == 1):
    		l1.append(p)
    	else:
    		l2.append(p)


def extract_file_code(f):
	str = ""
	for line in f:
		str += line
	return str


def build_incomplete_code_ast(file_name):
	f_incomplete = open(file_name)
	str_incomplete = ""
	str_incomplete = extract_file_code(f_incomplete)
	tree_incomplete = ast.parse(str_incomplete)
	prettyprint(tree_incomplete, 0, "", 2)

def iterate_directory(dir_name):
	for filename in os.listdir(dir_name):
		l1[:] = []
		f_complete = open(dir_name+'/'+filename)					#change it to backslash for unix based systems
		str_complete = extract_file_code(f_complete)
		tree_complete = ast.parse(str_complete)
		prettyprint(tree_complete, 0, "", 1)
		match_paths(filename)



def match_paths(filename):
	match = 0
	for w2 in l2:
		w2.strip()
		for w1 in l1:
			w1.strip()
			if(w2 in w1 and w2 != ' ') :
				match += 1
				#l1.remove(w1)
				break

	t = (float(match) * 100 ) / len(l2)
	d[filename] = t

if __name__ == "__main__":
	build_incomplete_code_ast(sys.argv[1])
	iterate_directory(sys.argv[2])
	print("Current File : ", sys.argv[1])
	print("Filename : \tMatching Percentage ")
	for filename, match in d.items():
		print(filename," : ", "{0:.2f}".format(round(match,2)))
