import hashlib
import random


class IdentificationFailure(Exception):
    pass


class Cipher:
    IDENTIFICATION = b'jl80ahs;df254LA;KFJ,mxnc9378'

    def __init__(self, key):
        self.method = None
        try:
            self.key = key.encode()
        except:
            self.key = key
        m = hashlib.sha1(self.key).hexdigest().encode()
        self.seed = int.from_bytes(m, byteorder='little') % 2**32
        random.seed(self.seed)
        self.encrypt_key = list(range(256))
        random.shuffle(self.encrypt_key)
        self.decrypt_key = {self.encrypt_key[i]: i for i in range(256)}

    def encrypt(self, data, check=False):
        try:
            data = data.encode()
        except:
            pass

        if check:
            data = self.IDENTIFICATION + data

        encrpted_data = bytes([self.encrypt_key[bit] for bit in data])
        return encrpted_data

        #return data

    def decrypt(self, data, check=False):

        try:
            data = data.encode()
        except:
            pass

        decrypt_data = bytes([self.decrypt_key[bit] for bit in data])

        if check:
            if decrypt_data[:len(self.IDENTIFICATION)] != self.IDENTIFICATION:
                raise IdentificationFailure

            decrypt_data = decrypt_data[len(self.IDENTIFICATION):]

        return decrypt_data

        #return data


def test():

    message = "You cannot see me!"
    key = "IJhphGHSLJDLFJSJjljlkajsf"
    cipher = Cipher(key)
    en = cipher.encrypt(message, True)
    print(en)
    cipher2 = Cipher(key)
    de = cipher2.decrypt(en, True)
    print(de.decode())


if __name__ == '__main__':
    test()
