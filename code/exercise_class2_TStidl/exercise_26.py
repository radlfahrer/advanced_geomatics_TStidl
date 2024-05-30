# exercise 26
print('exercise 26')

csvPath1 = "C:/Users/timo/Documents/Master/2_Semester/Advanced_geomatics/exercises/01_exe26_dataset1.csv"
with open(csvPath1, 'r') as file:
    lines = file.readlines()
    
data1Map = {}
for line in lines:
    line = line.strip()
    if line.startswith('#'):
        header1 = line
        continue
    lineSplit = line.split(",")
    id = int(lineSplit[0])
    x = float(lineSplit[1])
    y = float(lineSplit[2])
    values = [x,y]
    data1Map[id] = values

    
csvPath2 = "C:/Users/timo/Documents/Master/2_Semester/Advanced_geomatics/exercises/01_exe26_dataset2.csv"
with open(csvPath2, 'r') as file:
    lines = file.readlines()
    
data2Map = {}
for line in lines:
    line = line.strip()
    if line.startswith('#'):
        header2 = line
        continue
    lineSplit = line.split(",")
    id = int(lineSplit[0])
    z = float(lineSplit[1])
    data2Map[id] = z

completedataMap = data1Map


for key, value in data2Map.items():
    if key in completedataMap.keys():
        completedataMap[key] += [value]


IDs = list(completedataMap.keys())
IDs.sort()

print(f"{header1},{header2.split(',')[-1]}")
for id in IDs:
    x = completedataMap[id][0]
    y = completedataMap[id][1]
    value = completedataMap[id][2]
    print(f"{id},{x},{y},{value}")



