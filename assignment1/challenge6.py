import base64
from math import ceil
from math import floor

inp = input()
inp_bytes = base64.b64decode(inp)

frequencies = {
    'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
    'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
    'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
    'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
    'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
    'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
    'y': .01974, 'z': .00074, ' ': .13000
}

def evaluate_english_text(plain):
    score = 0
    for ch in plain:
        score += frequencies.get(ch.lower(), 0)

    return score

def getScore(tup):
    return tup[0]

def solve(inp):
    possible_english_texts = []
    c = inp
    for i in range((1 << 8) - 1):
        plain_text = [chr(x ^ i) for x in c]
        score = evaluate_english_text(plain_text)
        
        possible_english_texts.append((score, i))

    possible_english_texts = sorted(possible_english_texts, key=getScore)

    return possible_english_texts[len(possible_english_texts) - 1][1]

def xor(s1, s2):
    return bytes(a ^ b for a, b in zip(s1, s2,))

def hammingDistance(block1, block2):
    
    count = 0
    xor_bytes = xor(block1, block2)
    for diff_bits in xor_bytes:
        while(diff_bits > 0):
            if (diff_bits % 2 == 1):
                count += 1
            diff_bits = diff_bits >> 1

    return count
    
keyDistances = []
for keysize in range(2, 41):
    offset = 0
    distance = 0
    counter = 0
    while offset < len(inp_bytes) - keysize:
        distance += hammingDistance(inp_bytes[offset:offset + keysize], inp_bytes[offset + keysize:offset + 2 * keysize]) / keysize
        counter += 1
        offset += 2 * keysize;

    
    keyDistances.append((keysize,  distance / counter))

keyDistances.sort(key = lambda x : x[1])


def decipher(keysize):
    res = []
    for i in range(keysize):
        index = i
        block = []
        while (index < len(inp_bytes)):
            block.append(inp_bytes[index])
            index += keysize

        res.append(solve(block))

    return res

keys = []
for i in range(3):
    keysize = keyDistances[i][0]
    keys.append(decipher(keysize))

def repeatedXOR(key):
    result = ''.join([chr(a ^ b) for a, b in zip(inp_bytes, key * ceil(len(inp_bytes) / len(key)))])
    return result


possible_plain_texts = []
for key in keys:
    m = repeatedXOR(key)
    possible_plain_texts.append((evaluate_english_text(m), m))

possible_plain_texts.sort(key=lambda x: x[0]);

print(possible_plain_texts[len(possible_plain_texts) - 1][1])
