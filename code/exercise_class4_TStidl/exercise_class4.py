from pyqgis_scripting_ext.core import *


# exercise 03

folder = "C:/Users/timo/Documents/Master/2_Semester/Advanced_geomatics/TIMO_STIDL"

path = f"{folder}/stations.txt"

with open(path, 'r') as file:
    lines = file.readlines()
    
crsHelper = HCrs()
crsHelper.from_srid(4326)
crsHelper.to_srid(32632)

crsHelper2 = HCrs()
crsHelper2.from_srid(32632)
crsHelper2.to_srid(3857)
    
checkPoint = crsHelper.transform(HPoint(11.34999, 46.49809))
#checkPoint = HPoint(11.34999, 46.49809)

counter = 0

for line in lines:
    line.strip()
    lineSplit = line.split(',')
    if lineSplit[0].startswith('#'):
        continue
    counter += 1
    LAT = lineSplit[3]
    LATSplit = LAT.split(':')
    if LAT.startswith('+'):
        LATCoord = float(LATSplit[0]) + float(LATSplit[1])/60 + float(LATSplit[2])/3600
    else:
        LATCoord = float(LATSplit[0]) - float(LATSplit[1])/60 - float(LATSplit[2])/3600
    LON = lineSplit[4]
    LONSplit = LON.split(':')
    if LON.startswith('+'):
        LONCoord = float(LONSplit[0]) + float(LONSplit[1])/60 + float(LONSplit[2])/3600
    else:
        LONCoord = float(LONSplit[0]) - float(LONSplit[1])/60 - float(LONSplit[2])/3600
    stationPoint = crsHelper.transform(HPoint(LONCoord, LATCoord))

    if counter < 2:
        nearestStation = stationPoint
        stationName = lineSplit[1].strip()
    else:
        if checkPoint.distance(stationPoint) < checkPoint.distance(nearestStation):
            nearestStation = stationPoint
            stationName = lineSplit[1].strip()

print(f"{stationName} -> {crsHelper.transform(nearestStation, inverse = True)}")

# exercise 04
# with using a buffer

radius = 20
checkPoint = crsHelper.transform(HPoint(11.34999, 46.49809))


buffer = checkPoint.buffer(radius * 1000)

checkPoint2 = crsHelper2.transform(checkPoint)
buffer2 = crsHelper2.transform(buffer)

canvas = HMapCanvas.new()

osm = HMap.get_osm_layer()
canvas.set_layers([osm])

canvas.add_geometry(checkPoint2)
canvas.add_geometry(buffer2)

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
    LON = lineSplit[4]
    LONSplit = LON.split(':')
    if LON.startswith('+'):
        LONCoord = float(LONSplit[0]) + float(LONSplit[1])/60 + float(LONSplit[2])/3600
    else:
        LONCoord = float(LONSplit[0]) - float(LONSplit[1])/60 - float(LONSplit[2])/3600
    stationPoint = crsHelper.transform(HPoint(LONCoord, LATCoord))
    
    if buffer.contains(stationPoint):
        print(f"{lineSplit[1].strip()} ({int(checkPoint.distance(stationPoint)/1000)}km) -> {crsHelper.transform(stationPoint, inverse = True)}")
        canvas.add_geometry(crsHelper2.transform(stationPoint), 'blue')


canvas.set_extent([1200000, 5800000, 1350000, 5900000])

canvas.show()


