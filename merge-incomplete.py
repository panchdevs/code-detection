while i < len(lh):
    alist[k]=lh[i]
    i=i+1
    k=k+1

while i < len(lh) and j < len(rh):
    if lh[i] < rh[j]:
        alist[k]=lh[i]
        i=i+1
    else:
        alist[k]=rh[j]
        j=j+1
        k=k+1



while j < len(rh):
    alist[k]=rh[j]
    j=j+1
    k=k+1
print("Merging ",alist)
