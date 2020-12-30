from des import *

# Full ciphertext as bytes: b"\x90\x34\x08\xec\x4d\x95\x1a\xcf\xae\xb4\x7c\xa8\x83\x90\xc4\x75"
# Trying key 0FFFFD466D2205DCDh

k_bytes = bytes(bytearray.fromhex("ffffd466d2205dcd"))
key = DesKey(k_bytes)

print(key.decrypt(b"\x90\x34\x08\xec\x4d\x95\x1a\xcf\xae\xb4\x7c\xa8\x83\x90\xc4\x75"))