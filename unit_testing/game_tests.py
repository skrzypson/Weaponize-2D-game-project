import unittest
from pathfinding import path_optimization


class GameTests(unittest.TestCase):

    path_0 = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 3), (5, 3), (6, 3), (6, 4), (6, 5), (5, 6), (6, 7), (7, 7)]
    path_1 = [(0, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 4), (3, 3), (4, 3), (5, 4), (6, 5), (7, 6), (7, 7)]
    path_2 = [(0, 0), (0, 1), (0, 2), (1, 3), (2, 3), (3, 3), (4, 4), (5, 4), (6, 5), (7, 6), (7, 7)]

    path_3 = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 4), (6, 5), (7, 5), (8, 6), (9, 6), (10, 6), (11, 7), (12, 7),
             (13, 8), (14, 8), (14, 9), (14, 10), (14, 11), (13, 9), (14, 7), (13, 10), (13, 11), (14, 6), (13, 7),
             (15, 5), (16, 6), (16, 7), (16, 8), (17, 9), (18, 10)]
    path_4 = [(0, 0), (1, 1), (2, 1), (3, 1), (4, 2), (5, 2), (6, 3), (7, 3), (8, 4), (9, 4), (10, 5), (11, 5), (12, 5),
             (13, 5), (14, 5), (15, 5), (16, 6), (16, 7), (17, 7), (17, 8), (17, 9), (17, 10), (18, 10)]
    path_5 = [(0, 0), (1, 1), (2, 1), (3, 1), (4, 2), (5, 2), (6, 3), (7, 3), (8, 4), (9, 4), (10, 5), (11, 5), (12, 5),
             (13, 5), (14, 5), (15, 5), (16, 6), (16, 7), (16, 8), (17, 8), (18, 8), (18, 9), (18, 10)]

    def test_return_path_index_combinations(self):

        result = path_optimization.return_path_index_combinations(self.path_0, self.path_1, self.path_2)

        self.assertListEqual(result, [(0,1), (0,2), (1,2)])

    def test_calc_path_distances(self):

        result_0 = sum(path_optimization.calc_path_distances(self.path_0))
        result_1 = sum(path_optimization.calc_path_distances(self.path_1))
        result_2 = sum(path_optimization.calc_path_distances(self.path_2))

        self.assertEqual(result_0, 13.05)
        self.assertEqual(result_1, 14.46)
        self.assertEqual(result_2, 11.64)

    def test_assess_path_consistency(self):

        result_0 = path_optimization.assess_path_consistency(self.path_0)
        result_1 = path_optimization.assess_path_consistency(self.path_1)
        result_2 = path_optimization.assess_path_consistency(self.path_2)
        result_3 = path_optimization.assess_path_consistency(self.path_3)
        result_4 = path_optimization.assess_path_consistency(self.path_4)
        result_5 = path_optimization.assess_path_consistency(self.path_5)

        self.assertTrue(result_0, True)
        self.assertTrue(result_1, True)
        self.assertTrue(result_2, True)
        self.assertTrue(result_3, True)
        self.assertTrue(result_4, True)
        self.assertTrue(result_5, True)
