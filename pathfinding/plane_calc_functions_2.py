import math
import operator


def calculate_distances(coord, coord_dict, end_point, start_point=(0, 0)):
    # print("g: " + str(coord_dict[coord]["g"]))
    # print("h: " + str(coord_dict[coord]["h"]))
    # print("f: " + str(coord_dict[coord]["f"]))
    coord_dict[coord]["g"] = round(math.sqrt((coord[1] - start_point[1]) ** 2 + (coord[0] - start_point[0]) ** 2), 2)
    coord_dict[coord]["h"] = round(math.sqrt((end_point[1] - coord[1]) ** 2 + (end_point[0] - coord[0]) ** 2), 2)
    coord_dict[coord]["f"] = round(coord_dict[coord]["g"] + coord_dict[coord]["h"], 2)
    # print("g: " + str(coord_dict[coord]["g"]))
    # print("h: " + str(coord_dict[coord]["h"]))
    # print("f: " + str(coord_dict[coord]["f"]))


def get_neighbors(node, top_left_coord, bottom_right_coord):
    neighbors = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
    children = []

    for increment in neighbors:

        child = tuple(map(operator.add, node, increment))

        if any(coord < 0 for coord in tuple(map(operator.sub, child, top_left_coord))) or any(
                coord < 0 for coord in tuple(map(operator.sub, bottom_right_coord, child))):
            continue

        else:
            children.append(child)
            # print("child of node " + str(node) + " is " + str(child))

    # print(("valid children of {} : " + str(children)).format(node))
    return children


def calculate_path(first_point, second_point, top_left_point_in_plane, bottom_right_point_in_plane,
                   plane_matrix_original, initial_closed_set):

    start_point = first_point
    end_point = second_point
    top_left_point = top_left_point_in_plane
    bottom_right_point = bottom_right_point_in_plane
    plane_matrix = plane_matrix_original
    open_set = {start_point: plane_matrix.plane.get(start_point)}
    closed_set = initial_closed_set.copy()

    print("openset before: " + str(open_set) + '\n')
    print("closedset before: " + str(closed_set) + '\n')

    path = []
    path_not_found = True

    while open_set and path_not_found:

        # find node with the lowest f in the openlist
        temp_dict = {key: value.get("f") for key, value in open_set.items()}
        q = min(temp_dict, key=(lambda k: temp_dict[k]))
        temp_dict = None

        # print("q : " + str(q))

        open_set.pop(q)
        closed_set.update({q: plane_matrix.plane.get(q)})
        path.append(q)

        for child in get_neighbors(q, top_left_point, bottom_right_point):

            if child in open_set or child in closed_set:
                continue

            if child == end_point:
                print("child is end point! ")
                path.append(child)
                closed_set.update({child: plane_matrix.plane.get(child)})
                path_not_found = False

            else:
                open_set.update({child: plane_matrix.plane.get(child)})
                # print("child: " + str(child) + " " + str(openset[child]))
                # print("calculating..." + str(child))
                calculate_distances(child, open_set, end_point, q)
                open_set[child]["parent"] = q

    print("openset after: " + str(open_set) + '\n')
    print("closedset after: " + str(closed_set) + '\n')
    print("path: " + str(path))

    draw_plane(bottom_right_point, path, closed_set)
    return path


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
