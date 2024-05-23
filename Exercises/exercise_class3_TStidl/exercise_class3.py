from pyqgis_scripting_ext.core import *

# exercise 00

folder = "C:/Users/timo/Documents/Master/2_Semester/Advanced_geomatics/TIMO_STIDL"
path = f"{folder}/02_exe0_geometries.csv"

with open(path, 'r') as file:
    lines = file.readlines()

geometries = []
colorsList = []
sizeList = []

for i in range(len(lines)):
    line = lines[i].strip()
    lineSplit = line.split(';')
    size = int(lineSplit[-1])
    sizeList.append(size)
    
    if lineSplit[0] == 'point':
        colorsList.append('violett')
        pointCoords = lineSplit[1].split(',')
        geometries.append(HPoint(float(pointCoords[0]), float(pointCoords[1])))
    
    elif lineSplit[0] == 'line':
        colorsList.append('blue')
        lineCoords = lineSplit[1].split(' ')
        lineCoordsList = []
        for item in lineCoords:
            coords = item.split(',')
            coords[0] = float(coords[0])
            coords[1] = float(coords[1])
            lineCoordsList.append(coords)
        geometries.append(HLineString.fromCoords(lineCoordsList))
        
    elif lineSplit[0] == 'polygon':
        colorsList.append('red')
        polyCoords = lineSplit[1].split(' ')
        polyCoordsList = []
        for item in polyCoords:
            coords = item.split(',')
            coords[0] = float(coords[0])
            coords[1] = float(coords[1])
            polyCoordsList.append(coords)
        geometries.append(HPolygon.fromCoords(polyCoordsList))

# print(geometries)
# print(colorsList)
# print(sizeList)


canvas0 = HMapCanvas.new()

for i in range(len(geometries)):
    canvas0.add_geometry(geometries[i], colorsList[i], sizeList[i])

canvas0.set_extent([0, 0, 45, 45])
#canvas0.show()

#######################################################################


# exercise 01


zoneExtent = 6
utmGrid = []
mapExtent = [-180,-90,180,90]


for i in range(int(mapExtent[2]*2/zoneExtent)):
    coords = [[i*zoneExtent + mapExtent[0], mapExtent[1]], [i*zoneExtent+zoneExtent + mapExtent[0], mapExtent[1]], [i*zoneExtent+zoneExtent + mapExtent[0], mapExtent[3]],[i*zoneExtent + mapExtent[0], mapExtent[3]], [i*zoneExtent + mapExtent[0], mapExtent[1]]]
    utmGrid.append(HPolygon.fromCoords(coords))

canvas1 = HMapCanvas.new()


for i in utmGrid:
    canvas1.add_geometry(i)
    
canvas1.set_extent(mapExtent)
#canvas1.show()

#####################################################################

# exercise 02

path = f"{folder}/stations.txt"

with open(path, 'r') as file:
    lines = file.readlines()
    
#mapExtent = [-180,-90,180,90] #whole world
#mapExtent = [-30,28,75,85] # customized extent
mapExtent = [-1877994.66, 3638086.74, 3473041.38, 9494203.2]
lat_min = 9999
lat_max = 9999
lon_min = 9999
lon_max = 9999


stationsCount = []

crsHelper = HCrs()
crsHelper.from_srid(4326)
crsHelper.to_srid(3857)



canvas2 = HMapCanvas.new()
    
for line in lines:
    line.strip()
    lineSplit = line.split(',')
    if lineSplit[0].startswith('#'):
        continue
    LAT = lineSplit[3]
    LATSplit = LAT.split(':')
    if LAT.startswith('+'):
        LATCoord = float(LATSplit[0]) + float(LATSplit[1])/60 + float(LATSplit[2])/3600
    else:
        LATCoord = float(LATSplit[0]) - float(LATSplit[1])/60 - float(LATSplit[2])/3600
    if lat_min == 9999 or LATCoord < lat_min:
        lat_min = LATCoord
    if lat_max == 9999 or LATCoord > lat_max:
        lat_max = LATCoord
    LON = lineSplit[4]
    LONSplit = LON.split(':')
    if LON.startswith('+'):
        LONCoord = float(LONSplit[0]) + float(LONSplit[1])/60 + float(LONSplit[2])/3600
    else:
        LONCoord = float(LONSplit[0]) - float(LONSplit[1])/60 - float(LONSplit[2])/3600
    if lon_min == 9999 or LONCoord < lon_min:
        lon_min = LONCoord
    if lon_max == 9999 or LONCoord > lon_max:
        lon_max = LONCoord
    canvas2.add_geometry(crsHelper.transform(HPoint(LONCoord, LATCoord)))
    
    # stations count
    stationsCount.append(lineSplit[2])
    
    
min_point = crsHelper.transform(HPoint(lon_min,lat_min))
max_point = crsHelper.transform(HPoint(lon_max,lat_max))
print(min_point.asWkt())
print(max_point.asWkt())

min_maxExtent = [lon_min,lat_min,lon_max,lat_max]

osm= HMap.get_osm_layer()
canvas2.set_layers([osm])

canvas2.set_extent(mapExtent)
canvas2.show()



countMap = {}
setCount = set(stationsCount)
for country in setCount:
    #print(f"{country}: {stationsCount.count(country)}")
    countMap[country] = stationsCount.count(country)
sortList = sorted(countMap, key=countMap.get, reverse = True)

for i in sortList:
    print(f"{i}: {countMap[i]}")




