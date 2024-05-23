# exercise 01

from pyqgis_scripting_ext.core import *


# paths
nat_earth_folder = 'C:/Users/timo/Documents/Master/2_Semester/Advanced_geomatics/natural_earth_vector.gpkg/packages/'
stations_folder = 'C:/Users/timo/Documents/Master/2_Semester/Advanced_geomatics/exercise_class7_TStidl/'


geopackagePath = nat_earth_folder + 'natural_earth_vector.gpkg'
countriesName = 'ne_50m_admin_0_countries'
stationsPath = stations_folder + 'stations.txt'


# create scheme

fields = {
    'STAID': 'Intger',
    'STANAME': 'String',
    'CN': 'String',
    'HGHT': 'Integer'
}

stationsLayer = HVectorLayer.new('stations', 'Point', 'EPSG:4326', fields)

with open(stationsPath, 'r') as file:
    lines = file.readlines()

for line in lines:
    line = line.strip()
    if line.startswith('#'):
        continue
    lineSplit = line.split(',')
    staid = int(lineSplit[0].strip())
    staname = lineSplit[1].strip()
    cn = lineSplit[2].strip()
    hght = int(lineSplit[-1].strip())
    latSplit = lineSplit[3].strip().split(':')
    
    if float(latSplit[0]) >= 0:
        lat = float(latSplit[0]) + float(latSplit[1])/60 + float(latSplit[2])/3600
    else:
        lat = float(latSplit[0]) - float(latSplit[1])/60 - float(latSplit[2])/3600

    lonSplit = lineSplit[4].strip().split(':')
    if float(lonSplit[0]) >= 0:
        lon = float(lonSplit[0]) + float(lonSplit[1])/60 + float(lonSplit[2])/3600
    else:
        lon = float(lonSplit[0]) - float(lonSplit[1])/60 - float(lonSplit[2])/3600
        
    stationsLayer.add_feature(HPoint(lon, lat),[staid, staname, cn, hght])
    
path = stations_folder + 'stations.gpkg'

error = stationsLayer.dump_to_gpkg(path, overwrite=True)

if error:
    print(error)
    
#############################################################

# exercise 03

fields = {
    'country': 'String'
}

centroidsLayer = HVectorLayer.new('centroids', 'Point', 'EPSG:4326', fields)

countriesLayer = HVectorLayer.open(geopackagePath, countriesName)

nameIndexCountries = countriesLayer.field_index('NAME')
countriesFeatures = countriesLayer.features()

for feature in countriesFeatures:
    if feature.attributes[nameIndexCountries]:
        countryName = feature.attributes[nameIndexCountries]
        countryGeometry = feature.geometry
        countryCentroid = countryGeometry.centroid()

        
        centroidsLayer.add_feature(countryCentroid, [countryName])

        if not countryCentroid.intersects(countryGeometry):
            print(countryName)
        


path2 = stations_folder + 'centroids.gpkg'

error = centroidsLayer.dump_to_gpkg(path2, overwrite=True)

if error:
    print(error)

    
    