# exercise 9
print('exercise 9')

csvPath = "C:/Users/timo/Documents/Master/2_Semester/Advanced_geomatics/exercises/01_exe9_data.csv"
with open(csvPath, 'r') as file:
    lines = file.readlines()

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
for line in lines:
    line = line.strip()
    lineSplit = line.split(";")
    lineString2 = lineSplit[0]
    lineSplit2 = lineString2.split(",")
    if is_float(lineSplit2[0]):
        print(f"{lineSplit2[0]},{lineSplit2[1]}")

print('-------------------------')
# exercise 10
print('exercise 10')
for line in lines:
    line = line.strip()
    lineSplit = line.split(";")
    lineString2 = lineSplit[0]
    lineSplit2 = lineString2.split(",")
    if is_float(lineSplit2[0]):
        if float(lineSplit2[1]) <= 1000 and float(lineSplit2[1]) >=0:
            print(f"{lineSplit2[0]},{lineSplit2[1]}")