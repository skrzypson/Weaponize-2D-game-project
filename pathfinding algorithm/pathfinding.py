import math
import operator
import time
import plane_calc_functions

#definition of plane extents
top_left_point = (0,0)
bottom_right_point = (20,15)

closedset = {}
closedset.update({(15,6) : {"node" : None, "parent" : None, "g" : None, "h" : None, "f" : None}})
closedset.update({(15,7) : {"node" : None, "parent" : None, "g" : None, "h" : None, "f" : None}})
closedset.update({(15,8) : {"node" : None, "parent" : None, "g" : None, "h" : None, "f" : None}})
closedset.update({(15,9) : {"node" : None, "parent" : None, "g" : None, "h" : None, "f" : None}})
closedset.update({(15,10) : {"node" : None, "parent" : None, "g" : None, "h" : None, "f" : None}})
closedset.update({(15,11) : {"node" : None, "parent" : None, "g" : None, "h" : None, "f" : None}})
closedset.update({(15,12) : {"node" : None, "parent" : None, "g" : None, "h" : None, "f" : None}})
closedset.update({(14,12) : {"node" : None, "parent" : None, "g" : None, "h" : None, "f" : None}})
closedset.update({(13,12) : {"node" : None, "parent" : None, "g" : None, "h" : None, "f" : None}})
closedset.update({(12,12) : {"node" : None, "parent" : None, "g" : None, "h" : None, "f" : None}})
closedset.update({(11,12) : {"node" : None, "parent" : None, "g" : None, "h" : None, "f" : None}})
openset = {}

start_point = (0,0)
end_point = (18,10)

class plane:

    def __init__ (self, bottom_right_point):

        node=0
        self.plane = dict()
       
        for j in range(bottom_right_point[1]+1):

            for i in range(bottom_right_point[0]+1):

                self.plane.update({(i,j) : {"node" : node, "parent" : None, "g" : None, "h" : None, "f" : None}})
                node += 1

base_plane = plane(bottom_right_point)

start_to_end_path = plane_calc_functions.calculate_path(start_point, end_point, top_left_point, bottom_right_point, base_plane, closedset)
print("start to end path: " + str(start_to_end_path))

end_to_start_path = plane_calc_functions.calculate_path(end_point, start_point, top_left_point, bottom_right_point, base_plane, closedset)
print("end to start path: " + str(end_to_start_path))

print("\n")

#detect common sections in both paths

for nodes_set1 in start_to_end_path:

    for nodes_set2 in end_to_start_path[::-1]:

        if nodes_set1 == nodes_set2:

            print("indices: (" + str(start_to_end_path.index(nodes_set1)) + str(end_to_start_path[::-1].index(nodes_set2)) + "), nodes: " + str(nodes_set1))
