# For GeoPandas to work with Anaconda Python (3) distribution, or miniconda
# create a new separate environment and install geopandas there
# $ conda create --name GIS -c conda-forge python=3.6 fiona geopandas jupyter basemap pandas shapely
# Then activate it to run within that environment
# $ source activate GIS

import geopandas as geo
import pandas as pd
from shapely.geometry import Point
import os
import time

# Note: there are a lot of unnecessary print() statements just used for timing operations
start_time = time.time()

data_dir = '.'
tracts_dir = 'LA_CensusTracts'
tracts_file = 'CENSUS_TRACTS_2000.shp'

# This is the field we want to pull over from the shapefile with this spatial join
tract_id = 'CT00'
data_file = 'la_family_data.csv'
separator = ','
rows_limit = None
# Only reading in some of the columns for this operation
fam_col = 'familyid'
lon_col = 'longitude'
lat_col = 'latitude'
data_cols = [fam_col, lat_col, lon_col]

out_file = 'la_family_tracts.csv'
out_shape = 'la_family_points.shp'
out_shape_dir = 'la_family_SHP'

# Read in census tracts shapefile
print('Loading census tracts:', end='', flush=True)
start_t = time.time()
tracts = geo.read_file(os.path.join(data_dir, tracts_dir, tracts_file))
print(' {:.2f} s'.format(time.time()-start_t))

# Read in coordinate data and convert to GDF
print('Loading ethnicity data... :', end='', flush=True)
start_t = time.time()
# Be sure to read 'familyid' as a string or initial zeroes will be lost!
eth = pd.read_csv(os.path.join(data_dir,data_file), sep=separator, nrows=rows_limit, usecols=data_cols, dtype={'familyid': 'str'})
# Null locations screw up spatial join later
eth = eth.dropna(axis=0)
print(' {:.2f} s'.format(time.time()-start_t))
print(len(eth), ' rows')

print('Converting coordinates:', end='', flush=True)
start_t = time.time()
# Lat/Lon pairs need to be converted to a Point() data type
eth['coordinates'] = list(zip(eth[lon_col], eth[lat_col]))
eth.coordinates = eth.coordinates.apply(Point)
print(' {:.2f} s'.format(time.time()-start_t))

print('Reprojecting...:', end='', flush=True)
start_t = time.time()
gdf = geo.GeoDataFrame(eth, geometry='coordinates')
# Have to set the Coordinate Reference System (CRS) initialy to say it's been hand-coded lat/lon
gdf.crs = {'init': 'epsg:4326'}
# Then reproject to same CRS as tracts
gdf = gdf.to_crs(tracts.crs)
# Note: Faster to project the tracts instead once you have more than 400k data points!
# tracts = tracts.to_crs(gdf.crs)
print(' {:.2f} s'.format(time.time()-start_t))

# Do the spatial join ('within' just slightly faster than 'intersects' or 'contains')
# For points in a polygon shouldn't matter which operation you use
print('Spatial join...:', end='', flush=True)
start_t = time.time()
eth_tracts = geo.sjoin(gdf, tracts, how="left", op='within')
print(' {:.2f} s'.format(time.time()-start_t))

# Saving only the two fields that we need to output CSV
print('Saving file:', end='', flush=True)
start_t = time.time()
eth_tracts[[fam_col,tract_id]].to_csv(os.path.join(data_dir, out_file), index=False, encoding='utf-8')
print(' {:.2f} s'.format(time.time()-start_t))

# Also saving data to shapefile (into its own directory to help keep files together)
out_shape_dir_path = os.path.join(data_dir, out_shape_dir)
if not os.path.exists(out_shape_dir_path):
	os.mkdir(out_shape_dir_path)
print('Saving shapefile:', end='', flush=True)
start_t = time.time()
eth_tracts[['familyid', 'coordinates', 'CT00']].to_file(os.path.join(out_shape_dir_path, out_shape))
print(' {:.2f} s'.format(time.time()-start_t))

print('Done. Overall time = {:.2f} s'.format(time.time()-start_time))
