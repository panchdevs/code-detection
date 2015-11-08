n = 6
A,B = 1,1
for i in range(n-1):
	A,B = B,A+B
	print(A)