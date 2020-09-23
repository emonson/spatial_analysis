# Spatial Analysis in Python

This is a simple example of how to do a spatial join between a data
set of (latitude, longitude) pairs to an Esri shapefile to get the census
tract ID for each lat/lon pair using the Python 
[GeoPandas](http://geopandas.org/)
module without having to use QGIS or ArcPro.

## Python GIS Module Installation

If you're using the Anaconda Python 3 
[individual](https://www.anaconda.com/products/individual) or 
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

## Showcase notebook

The [SpatialAnalysisPython.ipynb](SpatialAnalysisPython.ipynb) Jupyter notebook is a
nice brief summary of two techniques:

1. A **spatial join** between an ESRI Shapefile of census tract boundaries and
individual geocoded address (latitude,longitude) points to see which tract each house
falls in.
1. Probing/**sampling raster data** at geographic points to find out how
much particulate matter is in the atmosphere at each census block group centroid.


## Individual example scripts

The [spatial_join_simple.py](spatial_join_simple.py) file shows a minimal example 
of the spatial join procedure.

The [spatial_join_timed.py](spatial_join_timed.py) script uses the same basic procedure, 
but includes timing of the stages of the routine. 
This script also lays out file and column names in 
variables at the top, which is a better general procedure rather than having them 
scattered throughout the script.
Only the necessary columns are loaded in to the [Pandas](https://pandas.pydata.org/) 
DataFrame from the CSV file.

## Performance timing

We ran a similar script with InfoUSA data and whole US census tracts shapefiles
on the DVS Lab machines with various numbers of rows of lat/lon pairs. The 
[GeoPandasArcProComparison.png](GeoPandasArcProComparison.png) file shows how 
long it took in ArcPro vs GeoPandas for
converting the coordinates to the `Point()` data type, for reprojecting the points into
the coordinate system of the census tracts, and for doing the spatial join.
