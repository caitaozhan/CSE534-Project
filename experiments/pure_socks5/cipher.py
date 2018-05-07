import hashlib
import numpy as np

class Cipher:
    def __init__(self, key):
        self.method = None
        try:
            self.key = key.encode()
        except:
            self.key = key
        m = hashlib.sha1(self.key).hexdigest().encode()
        self.seed = int.from_bytes(m, byteorder='little') % 2**32
        np.random.seed(self.seed)
        self.encrypt_key = np.random.permutation(256)
        self.decrypt_key = {self.encrypt_key[i]:i for i in range(256)}


    def encrypt(self, data):
        '''
        try:
            data = data.encode()
        except:
            pass
        encrpted_data = bytes([self.encrypt_key[bit] for bit in data])
        return encrpted_data
        '''
        return data

    def decrypt(self, data):
        '''
        try:
            data = data.encode()
        except:
            pass
        decrypt_data = bytes([self.decrypt_key[bit] for bit in data])

        return decrypt_data
        '''
        return data

def test():
    
    message = "哈哈"
    key ="LKjp9s3fD"
    cipher = Cipher(key)
    en = cipher.encrypt(message)
    print(en)
    de = cipher.decrypt(en)
    print(de)

if __name__ == '__main__':
    test()