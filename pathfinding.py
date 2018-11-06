import numpy as np

zero_area = np.zeros((100,100), np.int8)

for i in zero_area:
    print(i)

cost_map = np.random.randint(0, 2, (30, 30), np.int8)

for i in cost_map:
    print(i)

begining = (5,5)
end = (45, 40)

open_list = list()
closed_list = list()

