import math
from itertools import combinations

# returns array of pairs of path indices (path combination without repetition)
def return_path_index_combinations(*list_of_paths):

    path_comparison_pairs = combinations([ind for ind in range(0, len(list_of_paths))], 2)
    return list(path_comparison_pairs)


# returns array of section lengths for a particular path
def calc_path_distances(path):
    
    distances = []
    prev_node = None

    for node in path:

        if node == path[0]:

            distances.append(0.0)
            prev_node = node

        else:

            distance_from_prev_node = round(math.sqrt((node[1] - prev_node[1]) ** 2 + (node[0] - prev_node[0]) ** 2), 2)
            distances.append(distance_from_prev_node)
            prev_node = node

    return distances


def assess_path_consistency(path):

    path_consistent = True

    for index, node in enumerate(path):

        if index == 0:

            prev_node = node
            continue

        elif abs(node[1] - prev_node[1]) > 1 or abs(node[0] - prev_node[0]) > 1:

            path_consistent = False

        prev_node = node

    return path_consistent


# compares an array of paths and returns an array containing:
# - a dictionary of common nodes and their details,
# - an array of pairs of path indices
# - and an array of path total lengths
def compare_paths(*paths):

    path_comparison_pairs = return_path_index_combinations(*paths)
    path_pair_comparison_dict = {}
    path_lengths = [round(sum(calc_path_distances(path)), 2) for path in paths]
    path_distances = [calc_path_distances(path) for path in paths]
    prev_node = None

    for path_pair in path_comparison_pairs:

        print(path_pair)
        path_n = path_pair[0]
        path_compared_n = path_pair[1]
        path = paths[path_n]
        path_to_compare = paths[path_compared_n]
        common_nodes_list = {}
        common_section_number = 0

        for node_index, node in enumerate(path):

            for node_in_path_to_compare_index, node_in_path_to_compare in enumerate(path_to_compare):

                if node == node_in_path_to_compare:

                    sum_distance_to_node = round(
                        sum(path_distances[paths.index(path)][:node_index + 1]), 2)

                    sum_distance_to_node_in_path_to_compare = round(
                        sum(path_distances[paths.index(path_to_compare)][:node_in_path_to_compare_index + 1]), 2)

                    # if common nodes' list is not empty, check if the current node indices are greater than
                    # the previous common node idices by at least 2; this gives an indication to change the common
                    # section number due to the current common node belonging to a different common section
                    if common_nodes_list:

                        print(prev_node)
                        if (node_index - common_nodes_list[prev_node]["path node index"] > 1) \
                                and (node_in_path_to_compare_index
                                     - common_nodes_list[prev_node]["compare-path node index"] > 1):

                            common_section_number += 1

                    new_node_and_details = {

                        node : {

                            "path node index" : node_index,
                            "distance to path node" : sum_distance_to_node,
                            "compare-path node index" : node_in_path_to_compare_index,
                            "distance to compare-path node": sum_distance_to_node_in_path_to_compare,
                            "common section id" : common_section_number

                            }
                    }

                    common_nodes_list.update(new_node_and_details)

                    prev_node = node

                    # should be replaced by common_nodes_list dictionary
                    # common_nodes.append([node_index, sum_distance_to_node, node_in_path_to_compare_index,
                    #                      sum_distance_to_node_in_path_to_compare, common_section_number, node])

        path_pair_comparison_dict.update({path_pair : common_nodes_list})

    [print(k,v) for k,v in path_pair_comparison_dict.items()]# for h in v]

    return [path_pair_comparison_dict, path_comparison_pairs, path_lengths]


def create_optimal_paths(common_nodes_list, paths_list, path_comparison_pair_list, path_lengths):

    original_common_nodes_list = common_nodes_list
    optimal_path_list = [path for path in paths_list]
    print(path_comparison_pair_list)

    for path_comparison_pair in path_comparison_pair_list:

        path_pair_common_node_list = original_common_nodes_list[path_comparison_pair]

        path_pair_common_node_list = iter(path_pair_common_node_list.items())
        prev_common_node, prev_common_node_details = next(path_pair_common_node_list)

        # adds first node to optimized path
        optimized_path = [prev_common_node]

        for common_node, common_node_details in path_pair_common_node_list:

            # checks if the common node belongs to the pair of paths
            #if common_node_details["compared paths"] == path_comparison_pair:

            # if prev and current node don't belong to the same section (if new section)
            if common_node_details["common section id"] != prev_common_node_details["common section id"]:

                # if distance between prev and current section larger for first path
                if (common_node_details["distance to compare-path node"]
                        - prev_common_node_details["distance to compare-path node"]) \
                        <= (common_node_details["distance to path node"]
                            - prev_common_node_details["distance to path node"]):

                    for index in range(prev_common_node_details["compare-path node index"] + 1,
                                       common_node_details["compare-path node index"] + 1):

                        optimized_path.append(paths_list[path_comparison_pair[1]][index])
                        print("addition: " + str(paths_list[path_comparison_pair[1]][index]))

                # if distance between prev and current section larger for second path
                elif (common_node_details["distance to compare-path node"]
                        - prev_common_node_details["distance to compare-path node"]) \
                        > (common_node_details["distance to path node"]
                            - prev_common_node_details["distance to path node"]):

                    for index in range(prev_common_node_details["path node index"] + 1,
                                       common_node_details["path node index"] + 1):

                        optimized_path.append(paths_list[path_comparison_pair[0]][index])
                        print("addition: " + str(paths_list[path_comparison_pair[0]][index]))

            # else if current node and prev node belong to the same section (if same section)
            elif common_node_details["common section id"] == prev_common_node_details["common section id"]:

                optimized_path.append(common_node)

            prev_common_node, prev_common_node_details = common_node, common_node_details

        optimal_path_list.append(optimized_path)
        path_lengths.append(round(sum(calc_path_distances(optimized_path)),2))

    return optimal_path_list

def cut_extra_sections(path):

    reduced_path = path
    extra_nodes = []

    for index, node in enumerate(path):

        reduced_path.remove(node)

        if reduced_path:

            for rp_node in reduced_path:

                rp_index = path.index(rp_node)

                if abs(rp_index - index) > 1 and assess_path_consistency([node, rp_node]):

                    extra_section = [path[extra_node] for extra_node in range(index + 1, rp_index)]
                    extra_section_len = round(sum(calc_path_distances(extra_section)),2)
                    extra_nodes.append((extra_section_len, extra_section))

    return extra_nodes

p = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 4), (6, 5), (7, 5), (8, 6), (9, 6), (10, 6), (11, 7), (12, 7),
     (13, 8), (14, 8), (14, 9), (14, 10), (14, 11), (13, 9), (14, 7), (13, 10), (13, 11), (14, 6), (13, 7), (15, 5),
     (16, 6), (17, 7), (17, 8), (18, 9), (18, 10)]

c = cut_extra_sections(p)

[print(x) for x in c]

# common_nodes = compare_paths(path3, path4, path5)
# optimal_paths = create_optimal_paths(common_nodes[0], [path3, path4, path5], common_nodes[1], common_nodes[2])
# [print(optimal_path) for optimal_path in optimal_paths]
# [print(path_length) for path_length in common_nodes[2]]

# print(return_path_index_combinations(1,2,3,4))