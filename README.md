# GeoPandas spatial join example

This is a simple example of how to do a spatial join between a data
set of (latitude, longitude) pairs to an Esri shapefile to get the census
tract ID for each lat/lon pair using the Python 
[GeoPandas](http://geopandas.org/)
module without having to use QGIS or ArcPro.

## Python GIS Module Installation

If you're using the Anaconda Python 3 
[standard](https://www.anaconda.com/distribution/) or 
[miniconda](https://docs.conda.io/en/latest/miniconda.html)
distribution, it's easier to get everything working without library conflicts if you
create a separate environment for this GIS work. In the Anaconda Prompt type

```
conda create --name GIS -c conda-forge pandas geopandas fiona basemap shapely
```

then to "activate" this environment, type

```
conda activate GIS
```

## Example scripts

The [spatial_join_simple.py]() file shows a minimal example of the procedure. That's
a good place to start.

The [spatial_join_timed.py]() script uses the same basic procedure, but includes timing
of the stages of the routine. This script also lays out file and column names in 
variables at the top, which is a better general procedure rather than having them 
scattered throughout the script.
Only the necessary columns are loaded in to the [Pandas](https://pandas.pydata.org/) 
DataFrame from the CSV file.

## Timing

We ran a similar script with InfoUSA data and whole US census tracts shapefiles
on the DVS Lab machines with various numbers of rows of lat/lon pairs. The 
[GeoPandasArcProComparison.png]() file shows how long it took in ArcPro vs GeoPandas for
converting the coordinates to the `Point()` data type, for reprojecting the points into
the coordinate system of the census tracts, and for doing the spatial join.
