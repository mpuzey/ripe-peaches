import hashlib


def calculate_hash(string):
    hash_object = hashlib.sha256(string.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    print(hex_dig)


if __name__ == "__main__":

    calculate_hash('YOB')
