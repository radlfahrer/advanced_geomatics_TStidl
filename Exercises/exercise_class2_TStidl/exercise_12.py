# exercise 12a
print('exercise 12')
who = {
    "Daisy": 11,
    "Joe": 201,
    "Will": 23,
    "Hanna": 44
}
what = {
    44: "runs",
    11: "dreams",
    201: "plays",
    23: "walks"
}
where = {
    44: "to town.",
    11: "in her bed.",
    201: "in the livingroom.",
    23: "up the mountain."
}


for x,y in who.items():
    print(f"{x} {what[y]} {where[y]}")
    
print('--------------------')
# exercise 12b

who = {
    "Daisy": 11,
    "Joe": 201,
    "Will": 23,
    "Hanna": 44
}
what = {
    44: "runs",
    11: "dreams",
    201: "plays",
    23: "walks"
}
where = {
    "runs": "to town.",
    "dreams": "in her bed.",
    "plays": "in the livingroom.",
    "walks": "up the mountain."
}

for x,y in who.items():
    action = what[y]
    location = where[action]
    print(f"{x} {action} {location}")
