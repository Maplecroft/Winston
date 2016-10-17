=======
Winston
=======


.. image:: https://img.shields.io/pypi/v/winston.svg
    :target: https://pypi.python.org/pypi/winston
    :alt: Latest Release

.. image:: https://pyup.io/repos/github/maplecroft/winston/shield.svg
    :target: https://pyup.io/repos/github/maplecroft/winston/
    :alt: Updates

.. image:: https://pyup.io/repos/github/maplecroft/winston/python-3-shield.svg
    :target: https://pyup.io/repos/github/maplecroft/winston/
    :alt: Python 3


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

You can either use Winston on the command-line or as a module.

Command-line
------------

To see your options, simply::

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

Module
------

You can also use Winston in your code:

.. code-block:: pycon

    >>> import rasterio
    >>> from winston.stats import summary
    >>> from shapely.geometry import Point
    >>> src = rasterio.open('/path/to/raster.tif')
    >>> print summary(src)
    Summary(count=37324800, sum=49041320.0, mean=5.8627439, min=0.0, max=10.0, std=2.2037256)
    >>> print summary(src, bounds=(4, 6))
    Summary(count=37324800, sum=9569182.0, mean=5.1044292, min=4.0, max=5.9999995, std=0.56939822)
    >>> print summary(src, bounds=(4, 6), mean_only=True)
    5.09
    >>> print summary(src, Point(-2.36, 51.38).buffer(0.25))
    Summary(count=169, sum=1229.4401, mean=8.9740152, min=8.3602285, max=9.4269724, std=0.24473859)

Exporting results is reasonably simple with ``tablib``:

.. code-block:: pycon

    >>> import rasterio
    >>> import tablib
    >>> from winston.stats import summary
    >>> from shapely.geometry import Point
    >>> src = rasterio.open('/path/to/raster.tif')
    >>> shapes = [Point(x, y).buffer(0.25) for x, y in zip(range(5), range(5, 0, -1))]
    >>> summaries = [summary(src, shape) for shape in shapes]
    >>> d = tablib.Dataset()
    >>> d.dict = [s.__dict__ for s in summaries]
    >>> print d.headers
    ['count', 'sum', 'mean', 'min', 'max', 'std']
    >>> open('output.csv', 'w').write(d.csv)
