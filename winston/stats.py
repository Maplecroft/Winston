# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import numpy
import six

from collections import namedtuple

from rasterio.mask import mask

from shapely import wkt
from shapely.geometry import mapping, shape

from winston.utils import raster_to_shape

log = logging.getLogger(__name__)


Summary = namedtuple('Summary', 'count sum mean min max std')


def summary(raster, geometry=None, all_touched=False, mean_only=False,
            bounds=None, exclude_nodata_value=True):
    """Return ``ST_SummaryStats`` style stats for the given raster.

    If ``geometry`` is provided, we mask the raster with the given geometry and
    return the stats for the intersection. The parameter can be a GeoJSON-like
    object, a WKT string, or a Shapely geometry.

    If ``all_touched`` is set, we include every pixel that is touched by the
    given geometry. If set to ``False``, we only include pixels that are
    "mostly" inside the given geometry (the calculation is done by Rasterio).

    If ``mean_only`` is ``True`` we only return the mean value of the pixels,
    not the full set of stats.

    If ``bounds`` is passed, it should be a two-tuple of (min, max) to use for
    filtering raster pixels. If not provided, we exclude anything equal to the
    raster no data value.

    If ``mean_only`` is ``False``, we return a ``namedtuple`` representing the
    stats. All other attributes should be obvious and are consistent with
    PostGIS (``min``, ``max``, ``std``, etc).

    If ``mean_only`` is ``True``, we simply return a ``float`` or ``None``
    representing the mean value of the matching pixels.

    The ``exclude_nodata_value`` is consistent with ``ST_SummaryStats`` in that
    if it's ``True`` (default) we only count non-nodata pixels (or those pixels
    within ``bounds`` if defined). If it's ``False`` we return the count of all
    pixels.

    """
    def no_result(mean_only):
        if mean_only:
            return None
        else:
            return Summary(None, None, None, None, None, None)

    try:
        if geometry:
            # If it's a string, assume WKT
            if isinstance(geometry, six.string_types):
                geometry = wkt.loads(geometry)

            # If not already GeoJSON, assume it's a Shapely shape
            if not isinstance(geometry, dict):
                geojson = mapping(geometry)
            else:
                geojson = geometry
                geometry = shape(geometry)
            result, _ = mask(
                raster, [geojson], crop=True, all_touched=all_touched,
            )
            pixels = result.data.flatten()
        else:
            pixels = raster.read(1).flatten()
    except ValueError:
        return no_result(mean_only)

    raster_shape = raster_to_shape(raster)
    if not raster_shape.contains(geometry):
        log.warning(
            'Geometry {} is not fully contained by the source raster'.format(
                geometry,
            )
        )

    if bounds:
        score_mask = numpy.logical_and(
            numpy.greater_equal(pixels, bounds[0]),
            numpy.less_equal(pixels, bounds[1]),
        )
    else:
        score_mask = numpy.not_equal(pixels, raster.nodata),

    scored_pixels = numpy.extract(score_mask, pixels)
    if len(scored_pixels):
        if mean_only:
            return scored_pixels.mean()
        else:
            if exclude_nodata_value:
                count = len(scored_pixels)
            else:
                count = len(pixels)
            return Summary(
                count,
                scored_pixels.sum(),
                scored_pixels.mean(),
                scored_pixels.min(),
                scored_pixels.max(),
                scored_pixels.std(),
            )
    else:
        return no_result(mean_only)
