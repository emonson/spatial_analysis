import geopandas as geo
import pandas as pd
from shapely.geometry import Point
import os

# Read in census tracts shapefile
tracts = geo.read_file('LA_CensusTracts/CENSUS_TRACTS_2000.shp')

# Read family data
# Be sure to read 'familyid' as a string or initial zeroes will be lost!
# Only reading in some of the columns for this operation
data_cols = ['familyid','longitude','latitude']
eth = pd.read_csv('la_family_data.csv', sep=',', usecols=data_cols, dtype={'familyid': 'str'})

# Lat/Lon pairs need to be converted to a Point() data type
# We'll put these in a new column called 'coordinates'
eth['coordinates'] = list(zip(eth['longitude'], eth['latitude']))
eth['coordinates'] = eth['coordinates'].apply(Point)

# Convert to GeoDataFrame, specifying which column contains the geometry
gdf = geo.GeoDataFrame(eth, geometry='coordinates')
# Have to set the Coordinate Reference System (CRS) initialy to say it's been hand-coded lat/lon
gdf.crs = {'init': 'epsg:4326'}
# Then reproject to same CRS as tracts
gdf = gdf.to_crs(tracts.crs)

# Do the spatial join
eth_tracts = geo.sjoin(gdf, tracts, how="left", op='within')

# Saving only the two fields that we need to output CSV
eth_tracts[['familyid','CT00']].to_csv('la_family_tracts.csv', index=False, encoding='utf-8')

# Alternatively save data to shapefile for easier mapping
# Like to put shapefiles in their own directory since there are multiple files
if not os.path.exists('la_family_SHP'):
	os.mkdir('la_family_SHP')
eth_tracts[['familyid', 'coordinates', 'CT00']].to_file('la_family_SHP/la_family_points.shp')