# Answer To Question - 1, 2 & 4

import nltk
from nltk.corpus import words

nltk.download('words')
english_words = set(words.words())

file = open("Decrypted_text.txt","w")
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
    deciphered = ""

    for s in range(26):
        deciphered_text = decipher(text, s)
        valid_words = check_validity(deciphered_text)

        if valid_words > most_valid_words:
            best_shift_key = s
            most_valid_words = valid_words
            deciphered = deciphered_text

    return deciphered, best_shift_key


ciphered_text = "VZ FRYSVFU VZCNGVRAG NAQ N YVGGYR VAFRPHER V ZNXR ZVFGNXRF V NZ BHGF BS PBAGEBY NAQ NG GVZRF UNEQ GB UNAQYR OHG VS LBH PNAG UNAQYR ZR NG ZL JBEFG GURA LBH FHER NF URYYQBAQ QRFRER ZR NG ZL ORFG ZNEVYLA ZBAEBR"

deciphered_text, key = shift_value(ciphered_text)
print(deciphered_text)
file.write(f"{deciphered_text}\n")
print()

r = open("Encrypted Code.txt", 'r')
encrypted_code = r.readlines()
decrypted_code = ""

for i in encrypted_code:
    decrypted_code += decipher(i, key)

print(decrypted_code)
file.write(decrypted_code)

# Answer To Question - 3
#In Corrected_Code-3C.py
