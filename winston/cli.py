# -*- coding: utf-8 -*-

from __future__ import absolute_import

import click
import rasterio
import tablib

from functools import partial
from tabulate import tabulate

from shapely.wkt import loads as load_wkt
from shapely.geometry import mapping, Point

from winston.utils import buffer_point
from winston.stats import summary


@click.command()
@click.argument('fnames', nargs=-1)
@click.option('--not-all-touched', is_flag=True,
              help='Only include pixels that have centroids inside the area. '
                   'Default is to include all pixels touched by the area.')
@click.option('--proportional', 'radius_mode', flag_value='prop',
              help='Use a radius proportional to latitude')
@click.option('--fixed', 'radius_mode', flag_value='fixed', default=True,
              help='Always use a buffer radius of 25/111.13 degrees (default)')
@click.option('--radius', '-r', default=25.0,
              help='Point radius in km (pass zero to disable point buffering)')
@click.option('--bounds', '-b', nargs=2, type=float,
              help='Optional bounds for clipping values rather than using '
                   'the raster no data value')
@click.option('--mean-only', '-o', is_flag=True,
              help='Only return scores, not all summary stats')
@click.option('--meta', '-m', is_flag=True,
              help='Include metadata about the raster in the output')
@click.option('--wkt', '-w', multiple=True,
              help='WKT string (can be used multiple times)')
@click.option('--wkt-file', '-W',
              help='Text file containing WKT strings (one per line)')
@click.option('--csv-file', '-c',
              help='CSV file containing location data')
def main(fnames=None, not_all_touched=False, bounds=None, radius=None,
         radius_mode=None, mean_only=False, meta=False, wkt=None,
         wkt_file=None, csv_file=None):
    all_touched = not not_all_touched

    if not len(fnames):
        click.echo('No file names given. Exiting.')
        return

    geometries = []
    # First, parse any WKT strings passed in
    if wkt:
        geometries.extend([load_wkt(s) for s in wkt])

    # Next, read any WKT files (plain text, one WKT per line)
    if wkt_file:
        geometries.extend([load_wkt(l) for l in open(wkt_file).readlines()])

    # CSV must have either 'lat' and 'lon'/'lng' columns *or* a 'geom'/'wkt'
    # column, so you could include WKT for a geometry rather than coordinates.
    # We check for coords first, then geometries.
    if csv_file:
        d = tablib.Dataset()
        d.csv = open(csv_file).read()
        for record in d.dict:
            lon = record.get('lon', record.get('lng'))
            lat = record.get('lat')
            geom = record.get('geom', record.get('wkt'))
            if lon and lat:
                geometries.append(Point(float(lon), float(lat)))
            elif geom:
                geometries.append(load_wkt(geom))

    # Take any points and buffer them if radius is > 0.
    source_geometries = geometries
    if radius > 0:
        buf = partial(buffer_point, radius=radius, radius_mode=radius_mode)
        geometries = map(buf, geometries)

    # Turn all the geometry objects into GeoJSON for rasterio
    geometries = map(mapping, geometries)

    if bounds:
        click.echo(
            ' - reporting stats for pixels where {} <= x <= {}'.format(*bounds)
        )
    else:
        click.echo(
            ' - reporting stats for all pixels with values'
        )

    if not len(geometries):
        click.echo(
            ' - no geometries provided, reporting stats for the entire raster'
        )
        geometries = [None]
        source_geometries = ['Entire raster']
    else:
        if radius == 0:
            click.echo(' - points not buffered')
        else:
            if radius_mode == 'prop':
                click.echo(
                    ' - buffers ({}km) are proportional to latitude'.format(
                        radius,
                    )
                )
            else:
                click.echo(
                    ' - buffers fixed at a {}/111.13 degree radius'.format(
                        radius,
                    )
                )

        if all_touched:
            click.echo(
                ' - pixels counted if any part is inside the geometry'
            )
        else:
            click.echo(
                ' - pixels only counted if the centroid is inside the geometry'
            )

    rasters = []
    for fname in fnames:
        try:
            rasters.append(rasterio.open(fname))
        except Exception as ex:
            click.echo('Error loading {} ({}). Aborting.'.format(fname, ex))

    for raster in rasters:
        results = []

        # We keep the source geometries so we can return them with the results
        # rather than the buffered versions. We also pass the source to Dekker
        # because it does its own buffering.
        for src, geometry in zip(source_geometries, geometries):
            name = str(src)
            if len(name) > 28:
                name = name[:25] + '...'

            row = [name]

            stats = summary(raster, geometry, all_touched, mean_only, bounds)
            if mean_only:
                row.append(stats)
            else:
                row.extend(list(stats))

            results.append(row)

        headers = [
            'geometry',
        ]
        if not mean_only:
            headers.extend(
                ['count', 'scored', 'sum', 'mean', 'min', 'max', 'std']
            )
        else:
            headers.append('mean')

        click.echo()
        click.echo(raster.name)
        if meta:
            click.echo(tabulate(
                [
                    ('CRS', str(raster.crs)),
                    ('Bounds', raster.bounds),
                    ('Size', '{} x {}'.format(raster.width, raster.height)),
                    ('Tiled', raster.is_tiled),
                    ('Block size', '{} x {}'.format(*raster.block_shapes[0])),
                    ('Driver', raster.driver),
                    ('Data type', ', '.join(raster.dtypes)),
                    (
                        'Compression',
                        raster.compression.value if raster.compression else ''
                    ),
                ],
                ['Meta', 'Data'],
                tablefmt='psql',
            ))
        click.echo(tabulate(results, headers, tablefmt='psql'))


if __name__ == "__main__":
    main()
