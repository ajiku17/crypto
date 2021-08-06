from math import ceil

key = input()

def enc(key, plain_text):
    k = key * ceil(len(plain_text) / len(key))
    cipher_text = ''
    for i in range(len(plain_text)):
        cipher_text += '{:02x}'.format(ord(plain_text[i]) ^ ord(k[i]))

    return cipher_text

inp = input()

print(enc(key, inp))