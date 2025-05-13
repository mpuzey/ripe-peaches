import hashlib


def calculate_hash(string):
    hash_object = hashlib.sha256(string.encode("utf-8"))
    hex_dig = hash_object.hexdigest()
    return hex_dig
