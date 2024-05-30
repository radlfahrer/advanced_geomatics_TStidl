
from pyqgis_scripting_ext.core import *


# paths
nat_earth_folder = 'C:/Users/timo/Documents/Master/2_Semester/Advanced_geomatics/natural_earth_vector.gpkg/packages/'
geopackagePath = nat_earth_folder + 'natural_earth_vector.gpkg'
provincesName = 'ne_10m_admin_1_states_provinces'

data_folder = 'C:/Users/timo/Documents/GitHub/advanced_geomatics/Exercises/exercise_class8_TStidl/'
csvPath = data_folder + 'dpc-covid19-ita-regioni.csv'

with open(csvPath, 'r') as file:
    lines = file.readlines()
line1Split = lines[0].strip().split(',')
regionIndex = None
for i in range(len(line1Split)):
    if line1Split[i] == 'denominazione_regione':
        regionIndex = i

regions = []

for line in lines[1:]:
    line = line.strip()
    lineSplit = line.split(',')
    if lineSplit[regionIndex] not in regions:
        regions.append(lineSplit[regionIndex])

regionsMap = {}

#print(regions)

countriesLayer = HVectorLayer.open(geopackagePath, provincesName)
countriesLayer.subset_filter("admin = 'Italy'")
#print(countriesLayer.fields.items())
nameIndexCountries = countriesLayer.field_index('admin')
nameIndexRegions = countriesLayer.field_index('region')
countriesFeatures = countriesLayer.features()

#regions_gpkg = []
regions_gpkgMap = {}

for feature in countriesFeatures:
    if feature.attributes[nameIndexRegions] not in regions_gpkg:
        regions_gpkg.append(feature.attributes[nameIndexRegions])
        regions_gpkgMap[region] = []



#print(regions_gpkg)

same_name = []
different_name = []

for region in regions:
    if region in regions_gpkg:
        same_name.append(region)
    else:
        different_name.append(region)
print(same_name)
print(different_name)

conversionMap = {
    
}