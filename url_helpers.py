import re

URL_BASE = "https://api-v3.mbta.com/"

NON_UNRESERVED_REGEXP = r"[^a-zA-Z0-9-_.~]"

def url_encode_match(match):
    return "%{:X}".format(ord(match.group(0)))


def url_encode(s):
    return re.sub(NON_UNRESERVED_REGEXP, url_encode_match, str(s))


def make_q(params):
    bits = []

    for key in params.keys():
        bits.append(url_encode(key) + "=" + url_encode(params[key]))

    return "&".join(bits)
