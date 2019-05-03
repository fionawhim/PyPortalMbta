from url_helpers import make_q, URL_BASE

class Stop:
    def __init__(self, route_id, stop_id, stop_name):
        self.route_id = route_id
        self.stop_id = stop_id
        self.stop_name = stop_name

        self.predictions = None

    def load_predictions(self, wifi):
        prediction_url = (
            URL_BASE
            + "predictions?"
            + make_q(
                {
                    "page[limit]": 3,
                    "sort": "arrival_time",
                    "filter[route]": self.route_id,
                    "filter[stop]": self.stop_id,
                }
            )
        )

        response = wifi.get(prediction_url)
        response_json = response.json()

        self.predictions = []
        for p in response_json["data"]:
            self.predictions.append(p['attributes']['arrival_time'])

        response.close()


