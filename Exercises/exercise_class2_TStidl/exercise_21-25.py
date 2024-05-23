# exercise 21
print('exercise 21')

n = 10
m = 5
for i in range(n):
    print("*"*m)
    
print('-----------------')    

# exercise 22
print('exercise 22')

n = 10
counter = 0
for i in range(n):
    counter +=1
    print("*"* counter)

print('-----------------')  

# exercise 23
print('exercise 23')

n = 10
while n > 0:
    print("*" * n)
    n -= 1
 
print('-----------------')  

# exercise 24
print('exercise 24')

a = 10
sum = 0
for i in range (a+1):
    if i%2 == 0:
        print(i)
        sum += i
print(f" The sum is {sum}")

print('-----------------')  

# exercise 25
print('exercise 25')

numbers = [123, 345, 5, 3, 8, 87, 64, 95, 9, 10, 24, 54, 66]
sum = 0
for i in numbers:
    if i%2 == 0:
        print(i)
        sum += i
print(f"The sum is {sum}")