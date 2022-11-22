import random
from os import urandom
from typing import Callable, Tuple
from ecc.utils import int_length_in_byte
from ecc.curve import Curve, Point
from ecc.key import *

class ElGamal:
    def __init__(self, curve:Curve):
        self.curve = curve

    def gen_random_value(self) -> int:
        random.seed(urandom(1024))
        b = random.randint(1, self.curve.n)
        return b

    def generate_private_key(self):
        return gen_private_key(self.curve, urandom)
    
    def generate_public_key(self, private_key):
        return get_public_key(private_key, self.curve)
    
    def get_generator(self):
        return self.curve.G

    def encrypt(self, plaintext: bytes, public_key: Point,
                b: int) -> Tuple[Point, Point]:
        return self.encrypt_bytes(plaintext, public_key, b)

    def decrypt(self, private_key: int, C1: Point, C2: Point) -> bytes:
        return self.decrypt_bytes(private_key, C1, C2)

    def encrypt_bytes(self, plaintext: bytes, public_key: Point,
                      b: int) -> Tuple[Point, Point]:
        # Encode plaintext into a curve point
        M = self.curve.encode_point(plaintext)
        return self.encrypt_point(M, public_key, b)

    def decrypt_bytes(self, private_key: int, C1: Point, C2: Point) -> bytes:
        M = self.decrypt_point(private_key, C1, C2)
        return self.curve.decode_point(M)

    def encrypt_point(self, plaintext: Point, public_key: Point,
                      b: int) -> Tuple[Point, Point]:
        # Base point G
        G = self.curve.G
        M = plaintext
        #print(int_length_in_byte(M.x),int_length_in_byte(M.y))
        C1 = b * G
        C2 = M + b * public_key
       # print(int_length_in_byte(C2.x),int_length_in_byte(C2.y))
        return C1, C2

    def decrypt_point(self, private_key: int, C1: Point, C2: Point) -> Point:
        M = C2 + (self.curve.n - private_key) * C1
        return M