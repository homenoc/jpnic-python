import string
import random


def get_random(n):
    dat = string.digits + string.ascii_lowercase + string.ascii_uppercase
    return ''.join([random.choice(dat) for i in range(n)])


def json_to_req_format(dicts):
    str = ""
    for key in dicts:
        str += key + "=" + dicts[key] + '&'
    return str[:-1]


def get_value(data):
    if data is None:
        return ""
    return data
