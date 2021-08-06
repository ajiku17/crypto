from base64 import b64encode

inp = input()

print(b64encode(bytes.fromhex(inp)).decode())