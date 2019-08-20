# Spatial join example

This is a simple example of how to do a spatial join between a data
set of latitude,longitude pairs to an Esri shapefile to get the census
tract ID for each lat/lon pair using the Python 
[GeoPandas](http://geopandas.org/)
module without having to use QGIS or ArcPro.

## Installation

If you're using the Anaconda Python 3 
[standard](https://www.anaconda.com/distribution/) or 
[miniconda](https://docs.conda.io/en/latest/miniconda.html)
distribution, it's easier to get everything working without library conflicts if you
create a separate environment for this GIS work. In the Anaconda Prompt type

```
conda create --name GIS -c conda-forge python=3.7 fiona geopandas jupyter basemap pandas shapely
```

then to "activate" this environment, type

```
conda activate GIS
```

## Example

The `spatial_join_exmaple.py` file shows a simple example of the procedure.
Only the necessary columns are loaded in to the [Pandas](https://pandas.pydata.org/) 
DataFrame from the CSV file.
*(Note that there are a bunch of extra print statements to test the timing of the operations
that aren't necessary for running the code.)*

## Timing

We ran a similar script with InfoUSA data and whole US census tracts shapefiles
on the DVS Lab machines with various numbers of rows of lat/lon pairs. The 
`GeoPandasArcProComparison.png` file shows how long it took in ArcPro vs GeoPandas for
converting the coordinates to the Point() data type, for reprojecting the points into
the coordinate system of the census tracts, and for doing the spatial join.
