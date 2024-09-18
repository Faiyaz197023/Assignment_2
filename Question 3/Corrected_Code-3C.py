#Incorrect Code

"""
global_variable = 100
my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

def process_numbers():
    global global_variable
    local_variable = 5
    numbers = [1, 2, 3, 4, 5]

    while local_variable > 0:
        if local_variable % 2 == 0:
            numbers.remove(local_variable)
        local_variable -= 1

    return numbers

my_set = {1, 2, 3, 4, 5, 5, 4, 3, 2, 1}
result = process_numbers(numbers=my_set)

def modify_dict():
    local_variable = 10
    my_dict['key4'] = local_variable

modify_dict()

def update_global():
    global global_variable
    global_variable += 10

for i in range(5):
    print(i)
    i += 1

if my_set is not None and my_dict['key4'] == 10:
    print("Condition met!")

if 5 not in my_dict:
    print("5 not found in the dictionary!")

print(global_variable)
print(my_dict)
print(my_set)

"""


#Solution

"""
1. Incorrect Argument in process_numbers() Call
Problem: The function process_numbers() does not accept any arguments, but it is being called with numbers=my_set as an argument.

Solution: Remove the argument when calling the function, as process_numbers is not defined to accept any parameters.

2. Duplicate Elements in my_set
Problem: The set my_set contains duplicate elements (1, 2, 3, 4, 5 repeated), but sets automatically remove duplicates. Including duplicates is unnecessary.

Solution: Simplify the set definition to include only unique elements, as sets cannot have duplicates.

3. Incrementing Loop Variable (i += 1) has No Effect
Problem: Inside the for loop, i += 1 has no effect on the iteration because Python manages the loop variable i internally. The increment is redundant and does not affect the loop behavior.

Solution: Remove the unnecessary i += 1 line inside the loop.

4. Using Dictionary Key Check for 5
Problem: The condition if 5 not in my_dict checks for the presence of 5 as a key in the dictionary, but your dictionary only has string keys ('key1', 'key2', etc.). This condition will always be true because 5 is not a key in the dictionary.

Solution: Modify the condition to check for a valid key, such as 'key5', or if you're checking for a value of 5, adjust the logic accordingly.

5. Unnecessary Declaration:
Problem: There was unnecessary global variable declared in process_number function

Solution : Just remove it

6.Function not called:
Problem: update_global() was not called
Solution:Call the function
"""

global_variable = 100
my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

def process_numbers():
   # Unnecessary global variable declaration
    local_variable = 5
    numbers = [1, 2, 3, 4, 5]

    while local_variable > 0:
        if local_variable % 2 == 0:
            numbers.remove(local_variable)
        local_variable -= 1

    return numbers

my_set = {1, 2, 3, 4, 5}  # Simplified to remove duplicate elements

result = process_numbers()  # Removed the incorrect argument

def modify_dict():
    local_variable = 10
    my_dict['key4'] = local_variable

modify_dict()

def update_global(): #Function was not called
    global global_variable
    global_variable += 10

for i in range(5):
    print(i)  # Removed unnecessary i += 1

if my_set is not None and my_dict['key4'] == 10:
    print("Condition met!")

if 5 not in my_dict:
    print("5 not found in the dictionary!")  # Adjust this based on the intended check

print(global_variable)
print(my_dict)
print(my_set)
