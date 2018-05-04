import hashlib

class Cipher:
    def __init__(self, key):
        self.method = None

    def encrypt(self, data):

        return data

    def decrypt(self, data):
        return data

def test():
    cipher = Cipher()
    message = "asdfddkkdff"
    key ="LKjp9s3fD"
    en = cipher.encrypt(message, key)
    cipher.decrypt(en, )

if __name__ == '__main__':
    