import numpy as np
from skimage.morphology import disk
import skimage.filters.rank as sfr

r = 2
a = np.array([[1,3,1],[1,7,5],[1,7,3]])
print("a:")
print(a)
rows, cols = a.shape[0], a.shape[1]
for row in range(r-1, rows-r+2):
    for col in range(r-1, cols-r+2):
        mark = a[row-r+1 : row+1, col-r+1 : col+1]
        a[row-r+1][col-r+1] = min(np.min(mark,axis=0))

print("a1:")
print(a)

