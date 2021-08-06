freq = {}

inp = bytes.fromhex(input())

for b in inp:
	if b in freq:
		freq[b] += 1
	else:
		freq[b] = 1

for k in range(255):
	print(''.join([chr(x ^ y) for x, y in zip([k]*len(inp), inp)]))


print(freq)