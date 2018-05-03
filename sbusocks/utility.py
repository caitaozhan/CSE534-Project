import json

def int_from_bytes(bytes_object):
    return int.from_bytes(bytes_object, byteorder='big')

def read_config(filename):
    with open(filename, 'r') as handle:
        dictdump = json.loads(handle.read(), encoding='utf-8')
    return dictdump

if __name__ == '__main__':
    dic = read_config("client_config.json")
    print(dic)
    print(dic['local_port'])