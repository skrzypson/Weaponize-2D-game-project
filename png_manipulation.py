import numpy as np
from PIL import Image

width =100
height =100

#array = np.zeros([height, width, 3], dtype=np.uint8)

array = np.full([height, width, 3], 255, dtype=np.uint8)

for i in range(0,100):
    for j in range(0,100):
        array[i,j] = [255,np.random.rand(1,1)*255,np.random.rand(1,1)*255]
    #array[10,:] = [0, 128, 0]
print(array)

img = Image.fromarray(array)
img.save('img.png')