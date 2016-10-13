=======
History
=======

Unreleased changes
------------------

* Updated CLI defaults to be more... sane

0.2.3 (2016-10-13)
------------------

* Invert default value of ``all_touched`` flag to be consistent with Rasterio
* Added missing requirement (``six``) and reorganised requirements files

0.2.2 (2016-10-13)
------------------

* Bugfix in namedtuple parameter ordering (oops!)

0.2.1 (2016-10-12)
------------------

* Accept WKT strings as well as GeoJSON & Shapely geometries
* Fix the processing of 'no result' summaries

0.2.0 (2016-10-12)
------------------

``winston.stats.summary``:

* now accepts Shapely geometries as well as GeoJSON-like objects
* we no longer round results to 3 decimal places
* the stats are now returned as a ``namedtuple`` rather than a list

0.1.1 (2016-10-12)
------------------

* Minor packaging fixes.

0.1.0 (2016-10-12)
------------------

* First release on PyPI.
