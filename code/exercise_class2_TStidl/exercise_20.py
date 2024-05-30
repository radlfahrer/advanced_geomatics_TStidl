# exercise 20
print('exercise 20')

filePath = "C:/Users/timo/Documents/Master/2_Semester/Advanced_geomatics/exercises/station_data.txt"
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
counter = 0
value = []

for line in lines:
    line = line.strip()
    if line.startswith('#') or len(line) == 0:
        continue
    lineSplit = line.split(",")
    if lineSplit[0] not in stationIDs:
        stationIDs.append(lineSplit[0])
    counter += 1
    if int(lineSplit[-2]) == -9999:
        continue
    value.append(float(lineSplit[-2]))
    
file_name = filePath.split('/')[-1]

# printing summary

print(f"File info: {file_name}")
print('-----------------------')
print(f"Stations count: {len(stationIDs)}")
print(f"Avarage value: {int(sum(value) / len(value))}")
print("Available fields:")
for i in range(len(fieldNames)):
    print(f" -> {fieldNames[i]}\n")
print('First data lines:')
for line in lines[:6]:
    line = line.strip()
    lineSplit = line.split(',')
    print(f"\t\t{line}")