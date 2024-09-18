# Get input string with validation for minimum length of 16 characters
the_string = input("Enter the string (at least 16 characters long): ")

while len(the_string) < 16:
    the_string = input("The string is too short. Please enter at least 16 characters: ")

# Initialize lists to store numbers, letters, even numbers, and uppercase letters
Numbers = []
Letters = []
even_number_ascii = []
upper_letter_ascii = []

# Iterate through each character in the string
for i in the_string:
    ascii_val = ord(i)
    if 48 <= ascii_val <= 57:  # Check if the character is a digit
        Numbers.append(i)
        if int(i) % 2 == 0:  # Check if the number is even
            even_number_ascii.append(ascii_val)  # Append ASCII value of even number
    elif 65 <= ascii_val <= 90:  # Check if the character is an uppercase letter
        Letters.append(i)
        upper_letter_ascii.append(ascii_val)  # Append ASCII value of uppercase letter
    elif 97 <= ascii_val <= 122:  # Check if the character is a lowercase letter
        Letters.append(i)

# Output results
print("Numbers:", Numbers)
print("Letters:", Letters)
print("Even numbers in ASCII:", even_number_ascii)
print("Uppercase letters in ASCII:", upper_letter_ascii)

