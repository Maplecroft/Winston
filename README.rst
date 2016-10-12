=======
Winston
=======

A bit like the PostGIS ``ST_SummaryStats`` function for rasters on your filesystem.
Mostly we're just stringing together some awesome libraries:

- `Rasterio`_
- `Shapely`_
- `Numpy`_
- `Tablib`_


Install
=======

Activate your project virtual environment, and then::

    pip install winston

If you just want to use the command-line features, you could::

    pip install --user winston


Usage
=====

On the command-line::

    winston --help

For example, to get stats for all WKTs in a text file for a given raster::

    winston some_file.tif -f wkts.txt

or just for one point, including raster metadata::

    winston /path/to/data/*.tif -w 'POINT (-4.483545 54.150744)' -m

Since we require ``rasterio``, you can also use the ``rio`` command-line tool to inspect your rasters::

    rio insp /path/to/geo.tif

Read more in the `Rasterio docs`_.

.. _`Rasterio`: https://mapbox.github.io/rasterio/
.. _`Shapely`: http://toblerity.org/shapely/manual.html
.. _`Numpy`: http://docs.scipy.org/doc/numpy/
.. _`Tablib`: http://docs.python-tablib.org/en/latest/
.. _`Rasterio docs`: https://mapbox.github.io/rasterio/

You can also use Winston as a module::

    >>> import rasterio
    >>> from winston.stats import summary
    >>> src = rasterio.open('/path/to/raster.tif')
    >>> print summary(src)
    [37324800.0, 37324800.0, 281865888.0, 7.552, 3.45, 0.0, 10.0]
    >>> print summary(src, bounds=(4, 6))
    [37324800.0, 1772928.0, 9023566.0, 5.09, 0.573, 4.122, 5.929]
    >>> print summary(src, bounds=(4, 6), mean_only=True)
    5.09
