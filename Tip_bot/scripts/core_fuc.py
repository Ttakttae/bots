import json


def read_f(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data