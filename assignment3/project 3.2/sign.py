from oracle import *
from helper import *

n = 119077393994976313358209514872004186781083638474007212865571534799455802984783764695504518716476645854434703350542987348935664430222174597252144205891641172082602942313168180100366024600206994820541840725743590501646516068078269875871068596540116450747659687492528762004294694507524718065820838211568885027869

e = 65537

Oracle_Connect()

def egcd(a, b):
    if a == 0:
        return (1, 0)

    rec = egcd(b % a, a)
    quotient = b // a
    return (rec[1], rec[0] - (quotient * rec[1]))

def inverse(a, b):
    return egcd(a, b)[1] % b

def forge(msg):
    two_pow_64 = Sign(1)
    two_pow_64_inverse = inverse(two_pow_64, n)

    two_pow_65 = Sign(2)
    m_half = Sign(msg >> 1)
    return (m_half * (two_pow_65 * two_pow_64_inverse)) % n


msg = "Crypto is hard --- even schemes that look complex can be broken"

m = ascii_to_int(msg)

print forge(m)

Oracle_Disconnect()