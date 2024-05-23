# exercise 1
print('exercise 1')
age = 25
name = "Mario Rossi"
activity = "skating"
job = "engineer"

print(f"Hei I am {name}\nI am {age} and I love to go {activity}\nI work as an {job}")

print('-------------------------')
# exercise 2
print('exercise 2')
csvPath = "C:/Users/timo/Documents/Master/2_Semester/Advanced_geomatics/exercises/01_exe2_data.csv"
with open(csvPath, 'r') as file:
    lines = file.readlines()
for line in lines:
    line = line.strip() #removes white spaces
    lineSplit = line.split(";")
    #print(lineSplit)
    
    analogString = lineSplit[0]
    analogSplit = analogString.split(":")
    x1 = float(analogSplit[1])
    #print(x1)
    
    maxanalogString = lineSplit[2]
    x2 = float(maxanalogString.split(":")[1])
    #print(x2)
    
    maxvoltageString = lineSplit[1]
    y2 = float(maxvoltageString[11:])
    #print(y2)
    
# x2/x1 = y2/y1
y1 = y2*x1/x2
print(y1)

print('-------------------------')
# exercise 3
print('exercise 3')
string = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s"
new_string = string.replace(',', ';')
print(new_string)

print('-------------------------')
# exercise 4
print('exercise 4')
list = [ 1, 2, 3, 4, 5]
for number in list:
    print(number)

print('-------------------------')
# exercise 5
print('exercise 5')

for number in list:
    print(f"Number {number}")

print('-------------------------')
# exercise 6
print('exercise 6')

list2 = [ 10, 20, 30, 40, 50, 60, 70, 80, 90, 100 ]
for i in range(5):
    print(f"Number {list2[i]}")
    
print('-------------------------')    
# exercise 7
print('exercise 7')

list1 = [1, 2, 3, 4, 5]
list2 = ["first","second","third","fourth","fifth"]

for i in range(len(list1)):
    print(f"{list2[i]} is {list1[i]}")

print('-------------------------')    
# exercise 8
print('exercise 8')


string = """Lorem ipsum dolor sit amet, consectetur adipiscing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum."""

char_count = len(string)
char_w_space = len(string) - string.count(' ')
stringSplit = string.split(' ')
word_count= len(stringSplit)

print(f"Characters count: {char_count}\nCharacters count without spaces: {char_w_space}\nWord count : {word_count}")

