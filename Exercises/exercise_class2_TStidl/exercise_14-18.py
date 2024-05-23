# exercise 14
print('exercise 14')
filePath = "C:/Users/timo/Documents/Master/2_Semester/Advanced_geomatics/exercises/stations.txt"
with open (filePath, 'r') as file:
     lines = file.readlines()

# print first 20 lines
print(lines[:20])

print('-----------------------')
# exercise 15
print('exercise 15')

counter = 0
for line in lines:
    line = line.strip() #removes white spaces
    if line.startswith('#') or len(line) == 0:
        continue
    lineSplit = line.split(",")
    counter += 1    
print(counter)

print('-----------------------')

# exercise 16
print('exercise 16')


print(f'Number of columns: {len(lineSplit)}')

print('-----------------------')

# exercise 17
print('exercise 17')


for line in lines[:20]:
    line = line.strip()
    if line.startswith('#') or len(line) == 0:
        continue
    lineSplit = line.split(",")
    print(lineSplit[0], lineSplit[1])

print('-----------------------')

# exercise 18
print('exercise 18')


statHeight = []
for line in lines:
    line = line.strip()
    if line.startswith('#') or len(line) == 0:
        continue
    lineSplit = line.split(",")
    statHeight.append(float(lineSplit[-1]))
print(int(sum(statHeight) / len(statHeight)))
