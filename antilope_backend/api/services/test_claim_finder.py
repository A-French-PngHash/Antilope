from django.test import TestCase
import numpy as np
from .gpx_decoder import Trace
from .claim_finder import ClaimFinder
class ClaimFinderTestCase(TestCase):
    # given when then scheme
    def setUp(self):
        pass

    def assert_same_list_of_point(self, list1, list2):
        self.assertEqual(set([(round(i[0], 2), round(i[1], 2)) for i in list1]), set([(round(i[0], 2), round(i[1], 2)) for i in list2]))


    def test_should_claim_surounding_tiles_when_having_simple_segment(self):
        # Given simple segment
        points = np.array([[0.3, 0.8], [1.9, 1.1], [3, 2]])
        trace = Trace(points=points)
        claim_finder = ClaimFinder(trace)

        # When getting tiles alongside route 
        tiles = claim_finder.get_tiles_alongside_route(points)

        # Then should claim surrounding tiles
        surround = [(i, 0) for i in range(2)] + [(i, 1) for i in range(3)] + [(i, 2) for i in range(1, 4)]
        self.assert_same_list_of_point(surround, tiles)

    def test_should_claim_inside_tiles_when_having_simple_polygon(self):
        # Given simple polygon
        points = np.array([[1,1], [2.7, 1.5], [4.5, 0.5], [2, 3.5]]) # faire un schéma...
        trace = Trace(points=points)
        claim_finder = ClaimFinder(trace)

        # When getting inside tiles
        tiles = claim_finder.get_inside_tiles(points)

        # Then should claim inside tiles
        inside = [(2,3), (2,2), (3,2), (4,1)]
        self.assert_same_list_of_point(inside, tiles)

    def test_should_separate_well_when_having_a_trace_with_two_segment_and_a_loop(self):
        points = [(0.74, 0.48), (0.99, 0.44), (1.29, 0.55), (1.6, 0.56), (1.97, 0.65), (2.17, 0.79), (2.42, 0.95), (2.77, 1.13), (3.07, 1.28), (3.5, 1.55), (3.78, 1.76), (4.02, 2.02), (4.3, 2.29), (4.47, 2.48), (4.63, 2.67), (4.8, 2.82), (5.02, 2.98), (5.24, 3.21), (5.4, 3.5), (5.56, 3.81), (5.67, 4.06), (5.69, 4.43), (5.48, 5.0), (5.23, 5.46), (5.07, 5.55), (5.0, 5.63), (4.76, 5.71), (4.55, 5.74), (4.12, 5.66), (3.82, 5.48), (3.7, 5.01), (3.66, 4.77), (3.68, 4.43), (3.68, 4.13), (3.74, 3.77), (3.88, 3.36), (4.1, 3.06), (4.38, 2.77), (4.76, 2.56), (5.08, 2.48), (5.47, 2.41), (6.0, 2.33), (6.53, 2.29), (7.01, 2.25), (7.44, 2.24), (8.02, 2.26), (8.59, 2.4)]
        points = np.array([[i[0], i[1]] for i in points])
        trace = Trace(points=points)
        claim_finder = ClaimFinder(trace)

        # When separating
        tiles = claim_finder.separe(points)

        # Then should separate accordingly
        self.assert_same_list_of_point(points[0:13], tiles[0][1])
        self.assert_same_list_of_point(points[13:39], tiles[1][1])
        self.assert_same_list_of_point(points[39:], tiles[2][1])

        self.assertTrue(not tiles[0][0])
        self.assertTrue( tiles[1][0])
        self.assertTrue(not tiles[2][0])

    def test_should_return_segment_when_having_a_segment_trace_with_some_gaps(self):
        points = [(0.6, 0.47), (0.82, 0.37), (0.99, 0.45), (1.19, 0.51), (1.36, 0.55), (1.56, 0.61), (1.72, 0.68), (1.92, 0.76), (2.18, 0.94), (2.21, 0.97), (2.04, 0.95), (2.33, 1.06), (2.47, 1.16), (2.51, 1.21), (2.62, 1.26), (2.69, 1.33), (2.77, 1.4), (2.91, 1.59), (2.96, 1.66), (3.05, 1.82), (3.12, 1.95), (3.19, 2.13), (3.28, 2.36), (3.33, 2.56), (3.35, 2.9), (3.31, 3.21), (3.06, 3.54), (2.97, 3.64), (2.87, 4.0), (2.89, 4.21), (2.94, 4.29), (3.02, 4.38), (3.18, 4.48), (3.3, 4.5), (3.52, 4.48), (3.68, 4.44), (3.9, 4.35), (4.01, 4.27), (4.08, 4.2), (4.26, 4.06), (4.79, 3.77), (4.88, 3.71), (4.93, 3.73), (5.07, 3.67), (5.14, 3.66), (5.25, 3.62), (5.38, 3.55), (5.51, 3.47), (5.71, 3.37), (5.93, 3.23), (6.16, 3.0), (6.25, 2.87), (6.41, 2.72), (6.56, 2.6), (6.84, 2.45), (7.15, 2.47), (7.41, 2.48), (7.73, 2.62), (7.93, 2.77), (8.05, 2.97), (8.12, 3.35), (7.91, 5.4), (7.89, 6.66), (7.89, 7.46), (7.89, 7.62), (8.05, 8.3), (8.21, 8.41), (8.22, 8.47), (8.38, 8.58), (8.43, 8.6), (8.55, 8.61), (8.63, 8.61), (8.69, 8.58)]
        points = np.array([[i[0], i[1]] for i in points])
        trace = Trace(points=points)
        claim_finder = ClaimFinder(trace)

        # When separating
        tiles = claim_finder.separe(points)

        # Should detect a single segment
        self.assert_same_list_of_point(points, tiles[0][1])

        self.assertTrue(not tiles[0][0])

    def test_should_return_cycle_when_loop_trace(self):
        points = [(9.38, 8.97), (9.22, 8.96), (9.19, 8.96), (9.11, 8.96), (8.95, 8.96), (8.88, 8.96), (8.78, 8.95), (8.69, 8.95), (8.62, 8.95), (8.53, 8.95), (8.41, 8.95), (8.37, 8.96), (8.24, 8.96), (7.93, 8.95), (7.78, 8.91), (7.47, 8.85), (7.25, 8.83), (7.11, 8.8), (6.99, 8.73), (6.8, 8.66), (6.66, 8.61), (6.47, 8.53), (6.31, 8.42), (6.11, 8.31), (5.89, 8.19), (5.72, 8.1), (5.51, 7.89), (5.36, 7.69), (5.28, 7.46), (5.25, 7.28), (5.29, 7.01), (5.43, 6.7), (5.59, 6.35), (5.7, 6.15), (5.72, 5.82), (5.53, 5.38), (5.16, 5.15), (4.77, 5.16), (4.33, 5.34), (4.03, 5.5), (3.78, 5.69), (3.57, 5.75), (3.49, 6.4), (3.56, 6.73), (3.64, 6.88), (4.07, 7.13), (4.35, 7.18), (5.01, 7.12), (5.25, 7.04), (5.61, 6.93), (5.95, 6.84), (6.29, 6.76), (6.54, 6.72), (6.79, 6.66), (7.07, 6.59), (7.32, 6.55), (7.56, 6.55), (7.8, 6.58), (7.97, 6.61), (8.18, 6.72), (8.33, 6.8), (8.59, 6.96), (8.83, 7.15), (9.07, 7.42), (9.16, 7.54), (9.35, 8.01), (9.39, 8.2), (9.41, 8.47), (9.43, 8.8), (9.41, 8.87), (9.4, 8.99)]
        points = np.array([[i[0], i[1]] for i in points])
        trace = Trace(points=points)
        claim_finder = ClaimFinder(trace)

        # When separating
        tiles = claim_finder.separe(points)

        # Should detect a loop
        self.assert_same_list_of_point(points, tiles[0][1])
        self.assertTrue(tiles[0][0])


