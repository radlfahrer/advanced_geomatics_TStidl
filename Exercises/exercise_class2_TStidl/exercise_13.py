# exrercise 13
print('exercise 13')

list1 = ["a","b","c","d","e","f"]
list2 = ["c","d","e","f","g","h","a"]
list3 = ["c","d","e","f","g"]
list4 = ["c","d","e","h","a"]

joined_list = list1 + list2 + list3 + list4
unique_letters = list(set(joined_list))
unique_letters.sort()

for item in unique_letters:
    print(f"count of {item} = {joined_list.count(item)}")