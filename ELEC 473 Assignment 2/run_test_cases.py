from my_elgamal import ElGamal
from ecc.curve import secp256k1
from ecc.utils import int_length_in_byte
msg = "I am an undergraduate student at queen's university"
msg2 = "Hai-Ling Rao"
el = ElGamal(secp256k1)
sk = el.generate_private_key()
pk = el.generate_public_key(sk)
b = el.gen_random_value()
def encrypt(long_msg, b) -> list[bytes]:
    msg_bytes = list(bytes(long_msg, "utf-8"))
    msg_bytes.reverse()
    ciphertexts = list()
    def encrypt_block(msg_arr, b) -> bytes: 
        msg_bytes = bytes(msg_arr)
        #print(int_length_in_byte(sk))
        c1, c2 = el.encrypt(msg_bytes, pk, b)
        #print(c1)
        ciphertexts.append([c1,c2])

    while len(msg_bytes) >= 31:
        block = [msg_bytes.pop() for i in range(31)]
        encrypt_block(block,b)
    if msg_bytes:
        msg_bytes.reverse()
        encrypt_block(msg_bytes,b)
    return ciphertexts

def decrypt(ciphertexts):
    output = list()
    for c1, c2 in ciphertexts:
        decrypted = el.decrypt(sk, c1,c2).decode('utf-8')
        output.append(decrypted)
    print(''.join(output))
    return ''.join(output)

ciphertexts_1, ciphertexts_2 = encrypt(msg,b), encrypt(msg2,b)

decrypted_1, decrypted_2 = decrypt(ciphertexts_1), decrypt(ciphertexts_2)

assert msg == decrypted_1
assert msg2 == decrypted_2
print("Encryption and Decryption Successful")

#write values to file
with open('rand_value_b.txt', 'w') as f:
    f.write(str(b))
with open('pub_key.txt', 'w') as f:
    f.write(str(pk))
with open('pri_key.txt', 'w') as f:
    f.write(str(sk))
with open('generator.txt', 'w') as f:
    f.write(str(el.get_generator()))
with open('ciphertexts_1.txt', 'w') as f:
    f.writelines([str(txt)+'\n' for txt in ciphertexts_1])
with open('ciphertexts_2.txt', 'w') as f:
    f.writelines([str(txt)+'\n' for txt in ciphertexts_2])
with open('decrypted_plaintext_1.txt', "w") as f:
    f.write(decrypted_1)
with open('decrypted_plaintext_2.txt', "w") as f:
    f.write(decrypted_2)
