from oracle import *
import sys

if len(sys.argv) < 2:
    print "Usage: python sample.py <filename>"
    sys.exit(-1)

f = open(sys.argv[1])
data = f.read()
f.close()

ptext = [ord(x) for x in data]

blocks = []

soFar = []
for i in range(len(ptext)):
    if i % 16 == 0 and i > 0:
        blocks.append(soFar)
        soFar = []

    soFar.append(ptext[i])

if len(soFar) < 16:
    soFar += [0] * (16 - len(soFar))

blocks.append(soFar)

if len(blocks) % 2 != 0:
    print 'odd number of blocks'
    sys.exit(-1)

Oracle_Connect()

def XOR(x, y):
    return [a ^ b for a, b in zip(x,y)]


def toText(block):
    res = ''
    for b in block:
        res += chr(b)

    return res

t = Mac(toText(blocks[0] + blocks[1]), 2 * 16)
for i in range(2, len(blocks), 2):
    text = toText(XOR(t, blocks[i]) + blocks[i + 1])
    t = Mac(text, len(text))

ret = Vrfy(data, len(data), t)

if ret == 1:
    print "Message verified successfully!"
else:
    print "Message verification failed."

Oracle_Disconnect()
