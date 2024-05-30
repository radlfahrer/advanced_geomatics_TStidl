
from pyqgis_scripting_ext.core import *


# paths

data_folder = 'C:/Users/timo/Documents/GitHub/advanced_geomatics/data/'
csvPath = data_folder + 'dpc-covid19-ita-regioni.csv'
geopackagePath = data_folder + 'reduced_ne.gpkg'

provincesName = 'ne_10m_admin_1_states_provinces'

# gpkg combine provinces to regions

countriesLayer = HVectorLayer.open(geopackagePath, provincesName)
countriesLayer.subset_filter("admin = 'Italy'")
#print(countriesLayer.fields.items())
#nameIndexCountries = countriesLayer.field_index('admin')
nameIndexRegions = countriesLayer.field_index('region')
countriesFeatures = countriesLayer.features()

regions_gpkg = []
regions_gpkgMap = {}

for feature in countriesFeatures:
    geometry = feature.geometry
    region = feature.attributes[nameIndexRegions]
    if regions_gpkgMap.get(region):
        regions_gpkgMap[region].append()
    regions_gpkgMap[region] = []



print(regions_gpkgMap)


with open(csvPath, 'r') as file:
    lines = file.readlines()
line1Split = lines[0].strip().split(',')
regionIndex = None
for i in range(len(line1Split)):
    if line1Split[i] == 'denominazione_regione':
        regionIndex = i
        latIndex = i+1
        lonIndex = i+2

# regions = []
regionsMap = {}

crsHelper = HCrs()
crsHelper.from_srid(4326)
crsHelper.to_srid(3857)

#canvas = HMapCanvas.new()

#osm = HMap.get_osm_layer()
#canvas.set_layers([osm])

for line in lines[1:]:
    line = line.strip()
    lineSplit = line.split(',')
    if lineSplit[regionIndex] not in regions:
        regions.append(lineSplit[regionIndex])
    lon = float(lineSplit[lonIndex])
    lat = float(lineSplit[latIndex])
    
    #canvas.add_geometry(crsHelper.transform(HPoint(lon,lat)))

#canvas.show()



#print(regions)



same_name = []
different_name = []

for region in regions:
    if region in regions_gpkg:
        same_name.append(region)
    else:
        different_name.append(region)
#print(same_name)
#print(different_name)

conversionMap = {
    
}