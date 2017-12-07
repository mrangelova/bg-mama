import json


def jdefault(obj):
    return obj.__dict__


def encode(data):
    return json.dumps(data, default=jdefault, ensure_ascii=False)


def decode(data):
    return json.loads(data)
