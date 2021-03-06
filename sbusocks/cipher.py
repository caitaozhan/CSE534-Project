import hashlib
import random


class IdentificationFailure(Exception):
    pass


class Cipher:
    def __init__(self, key):
        self.method = None
        try:
            self.key = key.encode()
        except:
            self.key = key
        self.identification = hashlib.sha1(self.key).hexdigest().encode()
        self.seed = int.from_bytes(
            self.identification, byteorder='little'
        ) % 2**32
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
            data = self.identification + data

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
            try:
                assert (
                    decrypt_data[:len(self.identification)] ==
                    self.identification
                )
            except:
                raise IdentificationFailure

            decrypt_data = decrypt_data[len(self.identification):]

        return decrypt_data

        #return data


def test():

    message = "You cannot see me!"
    key = "IJhphGHSLJDLFJSJjljlkajsf"
    cipher = Cipher(key)
    print(cipher.identification)
    en = cipher.encrypt(message, True)
    print(en)
    cipher2 = Cipher(key + " ")
    de = cipher2.decrypt(en, True)
    print(de.decode())


if __name__ == '__main__':
    test()
