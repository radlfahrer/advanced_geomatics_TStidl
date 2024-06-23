
from pyqgis_scripting_ext.core import *


# paths

data_folder = 'C:/Users/timo/Documents/GitHub/advanced_geomatics/data/'
csvPath = data_folder + 'dpc-covid19-ita-regioni.csv'
geopackagePath = data_folder + 'reduced_ne.gpkg'
output_folder = 'C:/Users/timo/Documents/GitHub/advanced_geomatics/tmp/'

provincesName = 'ne_10m_admin_1_states_provinces'


# remove layers
HMap.remove_layers_by_name([provincesName])
# gpkg combine provinces to regions

countriesLayer = HVectorLayer.open(geopackagePath, provincesName)
countriesLayer.subset_filter("admin = 'Italy'")

#HMap.add_layer(countriesLayer)

#print(countriesLayer.fields.items())
#nameIndexCountries = countriesLayer.field_index('admin')
nameIndexRegions = countriesLayer.field_index('region')
countriesFeatures = countriesLayer.features()

regions_gpkgMap = {}

crsHelper = HCrs()
crsHelper.from_srid(4326)
crsHelper.to_srid(3857)

canvas = HMapCanvas.new()

osm = HMap.get_osm_layer()
canvas.set_layers([osm])

for feature in countriesFeatures:
    geometry = feature.geometry
    region = feature.attributes[nameIndexRegions]
    if regions_gpkgMap.get(region):
        regions_gpkgMap[region] = regions_gpkgMap[region].union(geometry)
    else:
        regions_gpkgMap[region] = geometry

for item in regions_gpkgMap.values():
    canvas.add_geometry(crsHelper.transform(item))

# csv file

with open(csvPath, 'r') as file:
    lines = file.readlines()
line1Split = lines[0].strip().split(',')
regionIndex = None
for i in range(len(line1Split)):
    if line1Split[i] == 'denominazione_regione':
        regionIndex = i
        latIndex = i+1
        lonIndex = i+2
    skip_addition = [i for i in range(len(line1Split)) if line1Split[i].startswith('note') or line1Split[i].startswith('codice')]

regionsMap = {}

# 0 (date), 3 (region), 17 (total cases)

day2featuresMap = {}

for index, line in enumerate(lines[1:]):
    line = line.strip()
    lineSplit = line.split(',')
    if not lineSplit[regionIndex].startswith('P.A'):
        region = lineSplit[regionIndex]
        lon = float(lineSplit[lonIndex])
        lat = float(lineSplit[latIndex])
        regionCity = HPoint(lon,lat)
    elif lineSplit[regionIndex].startswith('P.A. Bolzano'):
        continue
    else:
        region = 'Trentino-Alto Adige'
        lon = float(lineSplit[lonIndex])
        lat = float(lineSplit[latIndex])
        regionCity = HPoint(lon,lat)
        newlineSplit = []
        for i in range(len(lineSplit)):
            if i <= lonIndex or i >19:
                newlineSplit.append(lineSplit[i])
            else:
                if len(lineSplit[i]) == 0:
                    newlineSplit.append(lineSplit[i])
                    #continue
                else:
                    region_sum = int(lineSplit[i]) + int(lines[index-1].strip().split(',')[i])
                    newlineSplit.append(region_sum)
        lineSplit = newlineSplit
    dayAndTime = lineSplit[0]
    dayAndTime = dayAndTime.split('T')
    day = dayAndTime[0]
    if day.endswith('01'):
        totalCases = int(lineSplit[17])
        print(totalCases)
    
    for regionGeometry in regions_gpkgMap.values():
        if regionCity.intersects(regionGeometry):
            regionsMap[region] = regionGeometry
    canvas.add_geometry(crsHelper.transform(HPoint(lon,lat)))
canvas.set_extent(crsHelper.transform(item).bbox())
canvas.show()


#print(regionsMap)


featuresList = day2featuresMap.get(day)
if featuresList:
    featuresList.append()
