import operator
import math
import time
import random
from typing import List, Tuple, Deque, Set

from threading import Thread
from collections import deque


#top_left_coord = (0,0)
#bottom_right_coord = (175,20)

start_point = (0,0)
end_point = (100,100)

#l,h = min(top_left_coord), max(bottom_right_coord)

#random_walls = {(random.randint(l,h),random.randint(l,h)) for k in range(2000)}
one_line_wall = {(i,8) for i in range(10,41)}
enclosing_wall = {(19,0), (19,1), (20,1), (21,1), (21,0)}

#walls = {(3,5), (3,6), (3,7), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8), (8,7), (8,6), (8,5), (8,4), (7,4), (6,4),
#         (10,14), (10,13), (10,12), (10,11), (10,10), (10,9)}


class PathGenerator:

    def __init__(self, top_left_coord : Tuple[int, int], bottom_right_coord : Tuple[int, int]):

        self.top_left_coord = top_left_coord
        self.bottom_right_coord = bottom_right_coord

    neighbors_increment = {(1, 0), (0, 1), (0, -1), (-1, 0)}
    neighbors_increment_diag = {(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)}

    def drawPlane(self, _path, _obstacles={}):

        _plane = []

        for y in range(self.top_left_coord[1], self.bottom_right_coord[1] + 1):

            _row = []

            for x in range(self.top_left_coord[0], self.bottom_right_coord[0] + 1):

                if (x,y) in _path:

                    _row.append("o")

                elif (x,y) in _obstacles:

                    _row.append("X")

                else:

                    _row.append(".")

            _plane.append(_row)

        [print(''.join(row)) for row in _plane]
        print("\n")
        
    def distBetween(self, _current: Tuple[int, int], _neighbor: Tuple[int, int]) -> float:

        _dx = abs(_neighbor[1] - _current[1])
        _dy = abs(_neighbor[0] - _current[0])
        _dist = round(math.sqrt(_dx ** 2 + _dy ** 2), 2)

        return _dist

    def heuristicEstimate(self, _start_point: Tuple[int, int], _goal_point: Tuple[int, int]) -> float:

        _h = round(abs(_goal_point[1] - _start_point[1]) + abs(_goal_point[0] - _start_point[0]))

        return _h

    def neighborNodes(self, _node: Tuple[int, int], _top_left_coord: Tuple[int, int],
                      _bottom_right_coord: Tuple[int, int], _wall_encountered=False) -> List[Tuple[int, int]]:

        _children = []
        
        if _wall_encountered:
            
            _neighbors = self.neighbors_increment
            
        elif not _wall_encountered:
            
            _neighbors = self.neighbors_increment_diag

        for _increment in _neighbors:

            _child = tuple(map(operator.add, _node, _increment))

            if any(_coord < 0 for _coord in tuple(map(operator.sub, _child, _top_left_coord))) or any(
                    _coord < 0 for _coord in tuple(map(operator.sub, _bottom_right_coord, _child))):

                continue

            else:

                _children.append(_child)
            
        return _children

    def calc_path_distances(self, _path: List[tuple]) \
            -> List[float]:

        _distances = [0]

        for index, node in enumerate(_path[1::],1):

            _prev_node = _path[index - 1]
            _distance_from_prev_node = round(math.sqrt((node[1] - _prev_node[1]) ** 2 +
                                                       (node[0] - _prev_node[0]) ** 2), 2)
            _distances.append(_distance_from_prev_node)

        return _distances

    def diagonizePath(self, _path_input: List[Tuple[int, int]]) \
            -> List[Tuple[int, int]]:

        _path = list(_path_input)
        _path_even = _path[::2]
        _path_odd= _path[1::2]

        for index, node in enumerate(_path_even):

            if node == _path_even[-1]:
                    
                break

            elif tuple(map(operator.sub, node, _path_even[index + 1])) in self.neighbors_increment_diag:

                _path.remove(_path_odd[index])

        return _path
    
    def reconstructPath(self, _cameFrom: Set[Tuple[int, int]], _goal: Tuple[int, int]) \
            -> Deque[Tuple[int,int]]:
        
        _path = deque()
        _node = _goal
        _path.appendleft(_node)
        
        while _node in _cameFrom:
            
            _node = _cameFrom[_node]
            _path.appendleft(_node)
            
        return _path
    
    def getLowest(self, openSet: Set[Tuple[int,int]], fScore: float) \
            -> Tuple[int, int]:
        
        lowest = float("inf")
        lowest_node = None
        
        for node in openSet:
            
            if fScore[node] < lowest:
                
                lowest = fScore[node]
                lowest_node = node
                
        return lowest_node

    def aStar(self, _start_node: Tuple[int, int], _goal_node: Tuple[int, int], _wall_nodes: Set[Tuple[int, int]],
              result_array=None) -> Deque[Tuple[int, int]]:

        start_time = time.time()
        path_not_found = True
        _wall_encountered = _start_node in _wall_nodes
        came_from = {}
        open_set = set([_start_node])
        closed_set = set()
        g_score = {}
        f_score = {}
        g_score[_start_node] = 0
        f_score[_start_node] = g_score[_start_node] + self.heuristicEstimate(_start_node, _goal_node)
        
        while len(open_set) != 0 and path_not_found:

            current = self.getLowest(open_set, f_score)
            
            if current == _goal_node:

                path = self.reconstructPath(came_from, _goal_node)
                path = self.diagonizePath(path)
                
                if result_array != None:

                    result_array.append(path)

                return path

            open_set.remove(current)
            closed_set.add(current)
            neighbors = self.neighborNodes(current, self.top_left_coord, self.bottom_right_coord, _wall_encountered)

            _wall_encountered = any(neighbor in _wall_nodes for neighbor in neighbors)

            for neighbor in neighbors:

                if neighbor in _wall_nodes:

                    continue

                _tentative_gScore = g_score[current] + self.distBetween(current, neighbor)
                
                if neighbor in closed_set and _tentative_gScore >= g_score[neighbor]:
                    
                    continue
                
                if neighbor not in closed_set or _tentative_gScore < g_score[neighbor]:
                    
                    came_from[neighbor] = current
                    g_score[neighbor] = _tentative_gScore
                    f_score[neighbor] = g_score[neighbor] + self.heuristicEstimate(neighbor, _goal_node)
                    
                    if neighbor not in open_set:
                        
                        open_set.add(neighbor)

        return 0
