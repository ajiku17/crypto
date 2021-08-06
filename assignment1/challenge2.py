a = input()
b = input()

operands = [bytes.fromhex(z) for z in [a, b]]
print(''.join(['{:02x}'.format(x ^ y) for x, y in zip(operands[0], operands[1])]))
