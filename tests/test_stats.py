# -*- coding: utf-8 -*-

import rasterio
import os
import unittest

from shapely.wkt import loads
from winston.stats import summary, Summary


class TestSummaryStats(unittest.TestCase):
    def setUp(self):
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'data',
            'world.tif',
        )
        self.origin = loads('POINT(0 0)')
        self.src = rasterio.open(path)

    def test_point(self):
        result = summary(self.src, self.origin)
        expected = Summary(1, 1, 270, 270, 270, 270, 0)
        self.assertEqual(result, expected)

    def test_point_buffer(self):
        # world.tif looks like this:
        #
        # [   0,   90,  180,  270,  360]
        # [  45,  135,  225,  315,  405]
        # [  90,  180,  270,  360,  450]
        # [ 135,  225,  315,  405,  495]
        # [ 180,  270,  360,  450,  540]
        #
        # So a 45 degree buffer around the origin should be the nine pixels
        # from (1, 1) to (3, 3) in that matrix.

        result = summary(self.src, self.origin.buffer(45), all_touched=True)
        self.assertEqual(result.count, 9)
        self.assertEqual(result.data_count, 9)
        self.assertEqual(result.sum, 2430)
        self.assertEqual(result.mean, 270)
        self.assertEqual(result.min, 135)
        self.assertEqual(result.max, 405)
        self.assertAlmostEqual(result.std, 82.1584, 4)
