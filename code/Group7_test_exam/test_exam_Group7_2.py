from pyqgis_scripting_ext.core import *

def float_check(x):
    try:
        float(x)
        return True
    except ValueError:
        False


# folders and paths

folder1 = 'C:/Users/timo/Documents/Master/2_Semester/Advanced_geomatics/natural_earth_vector.gpkg/packages/'

geopackagePath = folder1 + 'natural_earth_vector.gpkg'
countriesName = 'ne_50m_admin_0_countries'

folder2 = 'C:/Users/timo/Documents/Master/2_Semester/Advanced_geomatics/Group7_test_exam/'
file_path = folder2 + '22yr_T10MN'
file_path2 = folder2 + '22yr_T10MX'

# read file

with open(file_path2, 'r') as file:
    lines = file.readlines()
    
# crs Helper

crsHelper = HCrs()
crsHelper.from_srid(4326)
crsHelper.to_srid(3857)

# countries 
country_variables = ['Germany', 'Austria', 'Switzerland', 'Italy']

countriesLayer = HVectorLayer.open(geopackagePath, countriesName)

nameIndex = countriesLayer.field_index('NAME')
countriesFeatures = countriesLayer.features()

geometries = []

for feature in countriesFeatures:
    name = feature.attributes[nameIndex]
    if name in country_variables:
        geometries.append(feature.geometry)

for i in range(len(geometries)):
    if i == 0:
        combined_geometry = geometries[0]
    else:
        combined_geometry = combined_geometry.union(geometries[i])

combined_geometry3857 = crsHelper.transform(combined_geometry)
       


# canvas

canvas = HMapCanvas.new()

#canvas.add_geometry(combined_geometry3857)

# add OSM

osm = HMap.get_osm_layer()
canvas.set_layers([osm])

# get min and max temp and then create a color ramp

# color ramp classes (max 6)

rampClasses = 6
colors = ['blue', 'green', 'yellow', 'orange', 'red', 'violet']


# choose month/annual
month_code = 'Ann'

features = {
'geometries': [],
'temperatures': [],
'colors': []
}

data_start = False
for line in lines:
    line = line.strip().strip('#')
    if line.lower().startswith('lat'):
        data_start = True
        lineSplit = line.split(' ')
        columns = [x.lower() for x in lineSplit if len(x) > 0]
        
        # get index
        month_index = columns.index(month_code.lower())
        continue
    if not data_start:
        continue
    lineSplit =line.split(' ')
    if not float_check(lineSplit[0]) or len(line)<1:
         continue
    
    tempValue = float(lineSplit[month_index])
    
    # extracting geometry
    lat = float(lineSplit[0])
    lon = float(lineSplit[1])
    

    point1 = (lon, lat)
    point2 = (lon + 1, lat)
    point3 = (lon + 1, lat + 1)
    point4 = (lon, lat + 1)
    coords = [point1, point2, point3, point4, point1]
    polygon = HPolygon.fromCoords(coords)
    
    if combined_geometry.intersects(polygon):
        polygon3857 = crsHelper.transform(polygon)
        features['geometries'].append(polygon3857)
        features['temperatures'].append(tempValue)
    

# get breaks of color ramp

temp_min = min(features['temperatures'])
temp_max = max(features['temperatures'])

class_width = (temp_max - temp_min) / rampClasses

tempClasses = []
for i in range(rampClasses):
    if i == 0:
        lowerLimit = float('-inf')
        upperLimit = temp_min + class_width * (i+1)
    elif i > 0 and i < rampClasses - 1:
        lowerLimit = temp_min + class_width * i
        upperLimit = temp_min + class_width * (i+1)
    elif i == rampClasses - 1:
        lowerLimit = temp_min + class_width * i
        upperLimit = float('inf')
    else:
        print('ERROR')
    tempClasses.append((lowerLimit, upperLimit))

# visualizing

for i in range(len(features['temperatures'])):
    temperature = features['temperatures'][i]
    
    for index, tempClass in enumerate(tempClasses):
        if temperature > tempClass[0] and temperature <= tempClass[1]:
            features['colors'].append(colors[index])

for index, geom in enumerate(features['geometries']):
    color = features['colors'][index]
    canvas.add_geometry(geom.intersection(combined_geometry3857), color)


canvas.set_extent(combined_geometry3857.bbox())
canvas.show()
        

