import ast
import re

l1 = []
l2 = []
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


f_complete = open("merge-complete.py")
f_incomplete = open("merge-incomplete.py")

str = ""
for line in f_complete:
	str += line

t = ast.parse(str)
#print("Tree 1 : \n")
prettyprint(t, 0, "",1)

for i, w in enumerate(l1):
	print(i,": ",w)

#print("Tree 1 : ")
str = ""
for line in f_incomplete:
	str += line

t = ast.parse(str)
#print("Tree 2 : \n\n")
prettyprint(t, 0, "",2)

#print(str)
print("Tree 2 : \n")
for i, w in enumerate(l2):
	print(i,": ",w)


match = 0
mx = 0
for w2 in l2:
	w2.strip()
	for w1 in l1:
		w1.strip()
		if(w2 in w1 and w2 != ' ') :
			match += 1
			l1.remove(w1)
			break

print("Total paths in incomplete code : ", len(l2))
print("Matched Paths : ",match)
print("Percentage : ", float(match) * 100 / len(l2) )