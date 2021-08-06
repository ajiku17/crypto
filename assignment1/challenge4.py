
n = int(input())

frequencies = {
    'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
    'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
    'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
    'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
    'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
    'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
    'y': .01974, 'z': .00074, ' ': .13000
};

def evaluate_english_text(plain):
    score = 0
    for ch in plain:
        score += frequencies.get(ch.lower(), 0)

    return score

def getScore(tup):
    return tup[0]

def solve(inp):
    possible_english_texts = []
    for i in range(inp):
        c = bytes.fromhex(input())
        for i in range((1 << 8) - 1):
            plain_text = [chr(x ^ i) for x in c]
            score = evaluate_english_text(plain_text)
            
            possible_english_texts.append((score, ''.join(plain_text),))

        possible_english_texts = sorted(possible_english_texts, key=getScore)

    return possible_english_texts[len(possible_english_texts) - 1][1]


print(solve(n))