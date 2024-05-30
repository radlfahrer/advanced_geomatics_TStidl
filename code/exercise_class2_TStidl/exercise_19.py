# exercise 19
print('exercise 19')

filePath = "C:/Users/timo/Documents/Master/2_Semester/Advanced_geomatics/exercises/stations.txt"
with open (filePath, 'r') as file:
     lines = file.readlines()
     
fields = lines[0]
fieldSplit = fields.split(',')
fieldNames = []
for field in fieldSplit:
    x = field.strip('#')
    y = x.strip()
    fieldNames.append(y)

stationIDs = []
statHeight = []

for line in lines:
    line = line.strip()
    if line.startswith('#') or len(line) == 0:
        continue
    lineSplit = line.split(",")
    if lineSplit[0] not in stationIDs:
        stationIDs.append(lineSplit[0])
    statHeight.append(float(lineSplit[-1]))
    
file_name = filePath.split('/')[-1]

# printing summary

print(f"File info: {file_name}")
print('-----------------------')
print(f"Stations count: {len(stationIDs)}")
print(f"Avarage value: {int(sum(statHeight) / len(statHeight))}")
print("Available fields:")
for i in range(len(fieldNames)):
    print(f" -> {fieldNames[i]}\n")
print('First data lines:')
for line in lines[:5]:
    line = line.strip()
    lineSplit = line.split(',')
    print(f"\t\t{line}")