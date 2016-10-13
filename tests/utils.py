#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rasterio
import numpy as np

from rasterio.transform import from_bounds


def generate_world_tif(path):
    x = np.linspace(0, 360, 5)
    y = np.linspace(0, 180, 5)
    X, Y = np.meshgrid(x, y)
    Z = X + Y

    # Z = array([[   0.,   90.,  180.,  270.,  360.],
    #            [  45.,  135.,  225.,  315.,  405.],
    #            [  90.,  180.,  270.,  360.,  450.],
    #            [ 135.,  225.,  315.,  405.,  495.],
    #            [ 180.,  270.,  360.,  450.,  540.]])

    transform = from_bounds(-180, -90, 180, 90, 5, 5)

    kwargs = dict(
        driver='GTiff',
        height=Z.shape[0],
        width=Z.shape[1],
        count=1,
        dtype=Z.dtype,
        crs='+proj=latlong',
        transform=transform,
    )
    with rasterio.open(path, 'w', **kwargs) as dst:
        dst.write(Z, 1)
