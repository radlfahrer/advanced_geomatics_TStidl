# exercise 11
print('exercise 11')
csvPath = "C:/Users/timo/Documents/Master/2_Semester/Advanced_geomatics/exercises/01_exe11_data.csv"
with open(csvPath, 'r') as file:
    lines = file.readlines()
for line in lines:
    line = line.strip('\n')
    line = line.replace('=', ';')
    lineSplit = line.split(';')
    lineSplit[1] = lineSplit[1].strip('cm')
    lineSplit[1] = float(lineSplit[1])
    lineSplit[3] = float(lineSplit[3]) * 100
    print(f"{lineSplit[0]} * {lineSplit[2]} / 2 = {lineSplit[1]} * {lineSplit[3]} / 2 = {lineSplit[1] * lineSplit[3] / 2}cm2")