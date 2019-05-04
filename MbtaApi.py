import re
import json

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

class MbtaApi:
    def __init__(self, wifi, lat, lng):
        self.wifi = wifi

        self.lat = lat
        self.lng = lng

    def get_nearest_stop(self, route_id, direction_id):
        stops_url = (
            URL_BASE
            + "stops?"
            + make_q(
                {
                    "page[limit]": 1,
                    "sort": "distance",
                    "include": "route",
                    "filter[route]": route_id,
                    "filter[direction_id]": direction_id,
                    "filter[latitude]": self.lat,
                    "filter[longitude]": self.lng,
                }
            )
        )

        response = self.wifi.get(stops_url)
        response_json = response.json()

        stop = response_json["data"][0]
        route = response_json["included"][0]

        response.close()

        return (stop, route)

    def get_predictions(self, route_id, stop_id):
        prediction_url = (
            URL_BASE
            + "predictions?"
            + make_q(
                {
                    "page[limit]": 3,
                    "sort": "arrival_time",
                    "filter[route]": route_id,
                    "filter[stop]": stop_id,
                }
            )
        )

        response = self.wifi.get(prediction_url)
        response_json = response.json()
        response.close()

        return response_json["data"]


class MbtaApiFake:
    def __init__(self):
        pass

    def get_nearest_stop(self, route_id, direction):
        with open("/fixtures/stops/" + route_id + ".json") as fp:
            str = fp.read()

        response_json = json.loads(str)

        stop = response_json["data"][0]
        route = response_json["included"][0]

        return (stop, route)
        
    def get_predictions(self, route_id, stop_id):
        with open("/fixtures/predictions/" + route_id + ".json") as fp:
            str = fp.read()

        return json.loads(str)["data"]
        
