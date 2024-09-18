import nltk
from nltk.corpus import words

nltk.download('words')
english_words = set(words.words())


def decipher(text, s):
    deciphered_text = ""

    for char in text:
        if 65 <= ord(char) <= 90:
            shifted_value = ord(char) + s

            if shifted_value > 90:
                shifted_value -= 26

            deciphered_text += chr(shifted_value)
        elif 97 <= ord(char) <= 122:
            shifted_value = ord(char) + s

            if shifted_value > 122:
                shifted_value -= 26

            deciphered_text += chr(shifted_value)
        else:
            deciphered_text += char

    return deciphered_text


def check_validity(text):
    words = text.split()
    total_valid = sum(1 for word in words if word.lower() in english_words)

    return total_valid


def shift_value(text):
    best_shift_key = 0
    most_valid_words = 0

    for s in range(26):
        deciphered_text = decipher(text, s)
        valid_words = check_validity(deciphered_text)

        if valid_words > most_valid_words:
            best_shift_key = s
            most_valid_words = valid_words

    return best_shift_key


r = open("Encrypted Code.txt", 'r')
encrypted_code = r.readlines()
filtered_encrypted_code = []
temp = ""

for i in encrypted_code:
    for char in i:
        if 65 <= ord(char) <= 90:
            temp += char

        elif 97 <= ord(char) <= 122:
            temp += char
        else:
            if temp:
                filtered_encrypted_code.append(temp)
                temp = ""

filtered_encrypted_code = " ".join(filtered_encrypted_code)

key = shift_value(filtered_encrypted_code)

decrypted_code = ""

for i in encrypted_code:
    decrypted_code += decipher(i, key)

print(decrypted_code)
