from oracle import *
import sys

if len(sys.argv) < 2:
    print "Usage: python2 decipher.py <file>"
    sys.exit(-1)

f = open(sys.argv[1])
data = f.read()
f.close()

ctext = [(int(data[i:i+2],16)) for i in range(0, len(data), 2)]

Oracle_Connect()

def get_block(ctext, block_ind):
    return ctext[block_ind * 16:(block_ind + 1) * 16]

def put_block(ctext, block_data, block_ind):
    for i in range(block_ind * 16, (block_ind + 1) * 16):
        ctext[i] = block_data[i - (block_ind * 16)]

def get_pad_mask(pad_len, g, guessed):
    if pad_len > 0:
        mask = [0] * 16
        for i in range(16 - pad_len, 16, 1):
            mask[i] ^= pad_len

        # print "pad mask before", mask
        for i in range(16 - len(guessed), 16, 1):
            mask[i] ^= guessed[i - (16 - len(guessed))]

        # print "pad mask after", mask
        mask[16 - pad_len] ^= g

        # print "pad mask final", mask

        return mask


def remove_pad(guessed_bytes):
    pad_len = guessed[len(guessed_bytes) - 1]
    for i in range(pad_len):
        guessed_bytes.pop(len(guessed_bytes) - 1)



def break_block(ctext, block_ind):
    guessed = []

    for pad_len in range (1, 16 + 1):
            # print "pad_len %d of block %d" % (pad_len, block_ind)
            for g in range (0, 256):
                if g == pad_len: 
                    continue

                copy = ctext[:]
                prev_block = get_block(copy, block_ind - 1)

                pad_mask = get_pad_mask(pad_len, g, guessed)
                # print "g = %d len(%d) pad_mask " % (g, len(pad_mask)), pad_mask
                # print "prev block before ", prev_block
                prev_block = [x ^ p for x, p in zip (prev_block, pad_mask)]
                # print "prev block after ", prev_block

                put_block(copy, prev_block, block_ind - 1)
                # print "g = %d len(%d) sending: " % (g, len(copy[:(block_ind + 1) * 16]) / 16), copy[:(block_ind + 1) * 16]
                rc = Oracle_Send(copy[:(block_ind + 1) * 16], len(copy[:(block_ind + 1) * 16]) / 16)
                # print "g = %d Oracle returned: %d" % (g, rc)
                if rc == 1:
                    guessed.insert(0, g)
                    print "guessed so far ", guessed
                    break;

    return guessed

def get_pad_index(ctext):
    offset = len(ctext) - 2 * 16
    for i in range (0, 16, 1):
        copy = ctext[:]
        copy[offset + i] = 9 #random number

        rc = Oracle_Send(copy, len(copy) / 16)
        if rc == 1:
            copy[offset + i] = 30 #random number
            # print "trying 30"
            rc = Oracle_Send(copy, len(copy) / 16)
            if rc == 1:
                continue

        return i

    return -1

def break_last_block(ctext):
    ind = len(ctext) / 16 - 1
    pad_index = get_pad_index(ctext[:])

    print "pad index", pad_index
    
    guessed = [16 - pad_index] * (16 - pad_index)

    for pad_len in range(16 - pad_index + 1, 16 + 1, 1):
        for g in range(0, 256):
            copy = ctext[:]
            prev_block = get_block(copy, ind - 1)

            pad_mask = get_pad_mask(pad_len, g, guessed)
            # print "g = %d len(%d) pad_mask " % (g, len(pad_mask)), pad_mask
            # print "prev block before ", prev_block
            prev_block = [x ^ p for x, p in zip (prev_block, pad_mask)]
            # print "prev block after ", prev_block

            put_block(copy, prev_block, ind - 1)
            # print "g = %d len(%d) sending: " % (g, len(copy) / 16), copy
            rc = Oracle_Send(copy, len(copy) / 16)
            # print "g = %d Oracle returned: %d" % (g, rc)
            if rc == 1:
                guessed.insert(0, g)
                print "guessed so far ", guessed
                break;

    return guessed
    

guessed = []
for i in range(1, len(ctext) / 16 - 1, 1):
    print "breaking block", i
    guessed += break_block(ctext, i)

print "breaking last block", i
guessed += break_last_block(ctext)

remove_pad(guessed)

print "Guessed!: ", guessed

mtext = ""
for b in guessed:
    mtext += chr(b)

print mtext

rc = Oracle_Send(ctext, len(ctext) / 16)
print "Oracle returned: %d" % rc 

Oracle_Disconnect()
