# -*- coding: utf-8 -*-

from __future__ import absolute_import

import numpy

from rasterio.mask import mask


def summary(raster, geometry=None, all_touched=True, mean_only=False,
            bounds=None):
    """Return ``ST_SummaryStats`` style stats for the given raster.

    If ``geometry`` is provided, we mask the raster with the given geometry and
    return the stats for the intersection.

    If ``all_touched`` is set, we include every pixel that is touched by the
    given geometry. If set to ``False``, we only include pixels that are
    "mostly" inside the given geometry (the calculation is done by Rasterio).

    If ``mean_only`` is ``True`` we only return the mean value of the pixels,
    not the full set of stats.

    If ``bounds`` is passed, it should be a two-tuple of (min, max) to use for
    filtering raster pixels. If not provided, we exclude anything equal to the
    raster no data value.

    If ``mean_only`` is ``False``, the values return correspond to::

        ['count', 'data_count', 'sum', 'mean', 'min', 'max', 'std']

    The difference betwee ``count`` and ``data_count`` is that ``data_count``
    is the count of all pixels that are either within ``bounds`` or not equal
    to the raster no data value.

    If ``mean_only`` is ``True``, we simply return a ``float`` or ``None``
    representing the mean value of the matching pixels.

    """
    def no_result(mean_only):
        if mean_only:
            return None
        else:
            return [0, None, None, None, None, None, None]

    try:
        if geometry:
            result, _ = mask(
                raster, [geometry], crop=True, all_touched=all_touched,
            )
            pixels = result.data.flatten()
        else:
            pixels = raster.read(1).flatten()
    except:
        return no_result(mean_only)

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
            return round(scored_pixels.mean(), 3)
        else:
            return map(lambda x: round(x, 3), [
                len(pixels),
                len(scored_pixels),
                scored_pixels.sum(),
                scored_pixels.mean(),
                scored_pixels.std(),
                scored_pixels.min(),
                scored_pixels.max(),
            ])
    else:
        no_result(mean_only)
