import math

path0 = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 4), (6, 5), (7, 5), (8, 6), (9, 6), (10, 6), (11, 7), (12, 7),
         (13, 8), (14, 8), (14, 9), (14, 10), (14, 11), (13, 9), (14, 7), (13, 10), (13, 11), (14, 6), (13, 7), (15, 5),
         (16, 6), (17, 7), (17, 8), (18, 9), (18, 10)]
path1 = [(0, 0), (1, 1), (2, 1), (3, 1), (4, 2), (5, 2), (6, 3), (7, 3), (8, 4), (9, 4), (10, 5), (11, 5), (12, 5),
         (13, 5), (14, 5), (15, 5), (16, 6), (16, 7), (16, 8), (17, 9), (18, 10)]


def calc_path_distances(path):
    distances = []
    prev_node = None

    for node in path:

        if node == path[0]:

            distances.append(0.0)
            prev_node = node

        else:

            distances.append(round(math.sqrt((node[1] - prev_node[1]) ** 2 + (node[0] - prev_node[0]) ** 2), 2))
            print(str(node) + " : " + str(
                round(math.sqrt((node[1] - prev_node[1]) ** 2 + (node[0] - prev_node[0]) ** 2), 2)))
            prev_node = node

    print(distances)
    print(sum(distances))

    return distances


# path0_distances = calc_path_distances(path0)
# path1_distances = calc_path_distances(path1)

def compare_paths(*paths):
    i = 0
    common_section_number = 0
    common_nodes = []
    path_distances = [calc_path_distances(path) for path in paths]
    print(path_distances)

    for path in paths:

        paths_to_compare = [path_to_compare for path_to_compare in paths if path != path_to_compare]

        for node in path:

            for path_to_compare in paths_to_compare:

                for node_in_path_to_compare in path_to_compare:

                    if node == node_in_path_to_compare:

                        node_index = path.index(node)
                        node_in_path_to_compare_index = path_to_compare.index(node_in_path_to_compare)
                        sum_distance_node = round(sum(path_distances[paths.index(path)][:node_index + 1]), 2)
                        sum_distance_node_in_path_to_compare = round(sum(path_distances[paths.index(path_to_compare)][:node_in_path_to_compare_index + 1]), 2)

                        if common_nodes:

                            if node_index - common_nodes[-1][0] > 1 and node_in_path_to_compare_index - common_nodes[-1][2] > 1:

                                common_section_number += 1

                        common_nodes.append([node_index, sum_distance_node, node_in_path_to_compare_index,
                                             sum_distance_node_in_path_to_compare, common_section_number, node])


        print("path " + str(i) + ": " + str(path))
        i += 1

        paths = [remaining_path for remaining_path in paths if remaining_path != path]

    return common_nodes


common_nodes = compare_paths(path0, path1)
[print(common_node_list) for common_node_list in common_nodes]

def optimize_path(common_nodes_array, pair_of_paths):

    common_nodes_array = iter(common_nodes_array)
    prev_common_node = next(common_nodes_array)
    optimized_path = [prev_common_node[5]]

    for common_node in common_nodes_array:

        if common_node[4] != prev_common_node[4]:

            if common_node[3] <= common_node[1]:

                for index in range(prev_common_node[2] + 1, common_node[2] + 1):

                    optimized_path.append(pair_of_paths[1][index])

            elif common_node[3] > common_node[1]:

                for index in range(prev_common_node[0] + 1, common_node[0] + 1):

                    optimized_path.append(pair_of_paths[1][index])

        elif common_node[4] == prev_common_node[4]:

            optimized_path.append(common_node[5])

        prev_common_node = common_node

    return optimized_path

optimized_path_example = optimize_path(common_nodes, [path0, path1])
print(optimized_path_example)





