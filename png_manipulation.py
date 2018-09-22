import numpy as np
from PIL import Image

width =1000
height =1000

#array = np.zeros([height, width, 3], dtype=np.uint8)

array = np.full([height, width, 3], 255, dtype=np.uint8)
#for q in range(0,100,1):
x = 0
for i in range(0,width,5):
    for j in range(0,height,5):
        array[i,j] = [255, np.random.ranf() * 255, np.random.ranf() * 255]
    #array[10,:] = [0, 128, 0]
#print(array)

img = Image.fromarray(array)
img.save('img.png')