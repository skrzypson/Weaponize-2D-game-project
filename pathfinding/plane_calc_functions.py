import math
import operator
from pathfinding import optimize_path


def calculate_distances(coord, coord_dict, end_point, start_point):
    # print("g: " + str(coord_dict[coord]["g"]))
    # print("h: " + str(coord_dict[coord]["h"]))
    # print("f: " + str(coord_dict[coord]["f"]))
    coord_dict[coord]["g"] = round(math.sqrt((coord[1] - start_point[1]) ** 2 + (coord[0] - start_point[0]) ** 2), 2)
    coord_dict[coord]["h"] = round(math.sqrt((end_point[1] - coord[1]) ** 2 + (end_point[0] - coord[0]) ** 2), 2)
    coord_dict[coord]["f"] = round(coord_dict[coord]["g"] + coord_dict[coord]["h"], 2)
    # print("g: " + str(coord_dict[coord]["g"]))
    # print("h: " + str(coord_dict[coord]["h"]))
    # print("f: " + str(coord_dict[coord]["f"]))


def return_calculated_distances(coord, end_point, start_point):

    g = round(math.sqrt((coord[1] - start_point[1]) ** 2 + (coord[0] - start_point[0]) ** 2), 2)
    h = round(math.sqrt((end_point[1] - coord[1]) ** 2 + (end_point[0] - coord[0]) ** 2), 2)
    f = round(g + h, 2)

    return {"g": g, "h" : h, "f" : f}


def return_g(coord, start_point):

    g = round(math.sqrt((coord[1] - start_point[1]) ** 2 + (coord[0] - start_point[0]) ** 2), 2)
    return g


def return_h(coord, end_point):

    h = round(math.sqrt((end_point[1] - coord[1]) ** 2 + (end_point[0] - coord[0]) ** 2), 2)
    return h


def return_f(g, h):

    f = round(g + h, 2)
    return f


# returns an array of nodes (tuples) that neighbor the input node
def get_neighbors(node, top_left_coord, bottom_right_coord):

    neighbors = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
    children = []

    for increment in neighbors:

        # perform tuple addition
        child = tuple(map(operator.add, node, increment))

        # if the neighbors are out of bounds, don't add to array
        if any(coord < 0 for coord in tuple(map(operator.sub, child, top_left_coord))) \
                or any(coord < 0 for coord in tuple(map(operator.sub, bottom_right_coord, child))):

            continue

        else:

            children.append(child)

    return children


# implementation of A* path finding algorithm
def calculate_path(start_point, end_point, top_left_point, bottom_right_point, plane_matrix, initial_closed_set):

    parent_nodes = {}
    open_set = {[start_point]}
    closed_set = initial_closed_set
    g_dist = {}
    f_dist = {}
    g_dist[start_point]
    f_dist[start_point] = g_dist[start_point] + return_h(start_point, end_point)

    while open_set:

        q = min(f_dist, key=(lambda k : f_dist[k]))

        if q == end_point:



    # start_point_h = return_calculated_distances(start_point, end_point, start_point)["h"]
    # start_node_details = {"node_no" : plane_matrix.plane[start_point]["node_no"], "parent": None, "g": 0,
    #                       "h": start_point_h, "f": start_point_h}
    #
    # open_set = {start_point: start_node_details}
    # closed_set = initial_closed_set.copy()
    # path = []
    # end_point_reached = True
    #
    # while end_point not in closed_set:
    #
    #     # find node with the lowest f in the open_list
    #     temp_dict = {key: value.get("f") for key, value in open_set.items()}
    #     q = min(temp_dict, key=(lambda k: temp_dict[k]))
    #     temp_dict = None
    #
    #     closed_set.update({q: open_set[q]})
    #     open_set.pop(q)
    #
    #     for child in get_neighbors(q, top_left_point, bottom_right_point):
    #
    #         g = closed_set[q]["g"] + return_g(child, q)
    #         h = return_h(child, end_point)
    #         f = return_f(g, h)
    #
    #         print(child)
    #
    #         if child == end_point:
    #
    #             print("child is end point! ")
    #
    #             child_end_point = {child: plane_matrix.plane.get(child)}
    #             child_end_point[child]["g"] = g
    #             child_end_point[child]["h"] = h
    #             child_end_point[child]["f"] = f
    #             child_end_point[child]["parent"] = q
    #             closed_set.update(child_end_point)
    #
    #         elif child in open_set and g < open_set[child]["g"]:
    #
    #             # open_set.pop(child)
    #             open_set[child]["g"] = g
    #             open_set[child]["h"] = h
    #             open_set[child]["f"] = f
    #             open_set[child]["parent"] = q
    #
    #         if child in closed_set and g < closed_set[child]["g"]:
    #
    #             closed_set[child]["g"] = g
    #             closed_set[child]["h"] = h
    #             closed_set[child]["f"] = f
    #             closed_set[child]["parent"] = q
    #
    #         if child not in open_set and child not in closed_set:
    #
    #             open_set.update({child : plane_matrix.plane.get(child)})
    #             open_set[child]["g"] = g
    #             open_set[child]["h"] = h
    #             open_set[child]["f"] = f
    #             open_set[child]["parent"] = q
    #
    # parents = {key: value.get("parent") for key, value in closed_set.items()}
    # reverse_path = [end_point]
    #
    # for parent in reverse_path:
    #
    #     reverse_path.append(closed_set[parent]["parent"])
    #
    #     if parent == start_point:
    #
    #         break
    #
    # path = reverse_path[::-1]
    #
    # print("openset after: " + str(open_set) + '\n')
    # print("closedset after: " + str(closed_set) + '\n')
    # print("path: " + str(path))
    #
    # draw_plane(bottom_right_point, path, closed_set)
    # return path


def draw_plane(bottom_right_point_in_plane, path_input, closedset_input):
    closedset = closedset_input
    path = path_input
    bottom_right_point = bottom_right_point_in_plane
    x = []

    for i in range(bottom_right_point[1] + 1):

        y = []
        x.append(y)

        for j in range(bottom_right_point[0] + 1):

            if (j, i) in path:
                y.append(1)
            elif (j, i) in closedset:
                y.append(7)
            else:
                y.append(0)
        print(y)
