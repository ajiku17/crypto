import math

def pow(base, exp, p):
	base_mod = base % p
	if exp == 0:
		return mod

	res = 1
	x = base_mod 
	y = 1
	while (exp > 1):
		if exp % 2 == 0:
			x *= x
			x %= p
			exp /= 2
		else:
			y *= x
			y %= p
			exp -= 1

	return (x * y) % p

# power mod p -> inverse mod -> multiply mod p
# Find x such that g^x = h (mod p)
# 0 <= x <= max_x
def discrete_log(g, h, p, max_x):
	B = int(math.ceil(math.sqrt(max_x)))

	g_inverse = pow(g, p - 2, p)
	table = dict()
	z = h
	for i in range(B):
		table[z] = i 	
		z = (z * g_inverse) % p
		
	g_B = pow(g, B, p)
	lhs = 1
	for i in range(B):
		if lhs in table:
			print table[lhs] + i * B
			break

		lhs *= g_B
		lhs %= p

def main():
	p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171
	g = 11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568
	h = 3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333
	max_x = 1 << 40 # 2^40
	discrete_log(g, h, p, max_x)

if __name__ == '__main__':
	main()

