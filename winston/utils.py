# -*- coding: utf-8 -*-

from __future__ import absolute_import

import math

from shapely.geometry import Point, Polygon


def km_to_degrees(km, latitude=None):
    if not latitude:
        return km / 111.13
    else:
        earth_radius = 6371.0
        degrees_to_radians = math.pi / 180.0
        radians_to_degrees = 180.0 / math.pi
        r = earth_radius * math.cos(latitude * degrees_to_radians)
        return (km / r) * radians_to_degrees


def buffer_point(geometry, radius, radius_mode):
    if isinstance(geometry, Point) and radius > 0:
        if radius_mode == 'fixed':
            return geometry.buffer(km_to_degrees(radius))
        else:
            return geometry.buffer(
                km_to_degrees(radius, geometry.coords[0][1])
            )
    else:
        return geometry


def raster_to_shape(raster):
    """Take a raster and return a polygon representing the outer edge."""
    left = raster.bounds.left
    right = raster.bounds.right
    top = raster.bounds.top
    bottom = raster.bounds.bottom

    top_left = (left, top)
    top_right = (right, top)
    bottom_left = (left, bottom)
    bottom_right = (right, bottom)

    return Polygon((
        top_left, top_right, bottom_right, bottom_left, top_left,
    ))
