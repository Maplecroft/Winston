# -*- coding: utf-8 -*-

import rasterio
import numpy
import os
import unittest

from shapely.geometry import mapping
from shapely.wkt import loads
from winston.stats import summary, Summary


class TestSummaryStats(unittest.TestCase):
    def setUp(self):
        # world.tif looks like this:
        #
        # [   0,   90,  180,  270,  360]
        # [  45,  135,  225,  315,  405]
        # [  90,  180,  270,  360,  450]
        # [ 135,  225,  315,  405,  495]
        # [ 180,  270,  360,  450,  540]
        #
        # Each pixel is 72x36 degrees and the origin is in the center of a
        # pixel.
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'data',
            'world.tif',
        )
        self.origin = loads('POINT(0 0)')
        self.src = rasterio.open(path)

    def test_point_wkt(self):
        result = summary(self.src, self.origin.wkt)
        expected = Summary(1, 270, 270, 270, 270, 0)
        self.assertEqual(result, expected)

    def test_point_geometry(self):
        result = summary(self.src, self.origin.wkt)
        expected = Summary(1, 270, 270, 270, 270, 0)
        self.assertEqual(result, expected)

    def test_point_geojson(self):
        result = summary(self.src, mapping(self.origin))
        expected = Summary(1, 270, 270, 270, 270, 0)
        self.assertEqual(result, expected)

    def test_out_of_bounds(self):
        top_left = loads('POINT(-181 91)')
        result = summary(self.src, top_left)
        expected = Summary(None, None, None, None, None, None)
        self.assertEqual(result, expected)

    def test_range(self):
        result = summary(self.src, self.origin, bounds=(0, 1))
        expected = Summary(None, None, None, None, None, None)
        self.assertEqual(result, expected)

    def test_origin_buffer(self):
        # A 45 degree buffer around the origin should be the nine pixels from
        # (1, 1) to (3, 3) in that matrix.

        expected = numpy.array([
            135, 225, 315,
            180, 270, 360,
            225, 315, 405,
        ])

        result = summary(self.src, self.origin.buffer(45), all_touched=True)
        self.assertEqual(result.count, expected.size)
        self.assertEqual(result.sum, expected.sum())
        self.assertEqual(result.mean, expected.mean())
        self.assertEqual(result.min, expected.min())
        self.assertEqual(result.max, expected.max())
        self.assertEqual(result.std, expected.std())
