from udatetime import datetime

class Stop:
    def __init__(self, mbta_api, route_id, direction_name, stop_id, stop_name):
        self.mbta_api = mbta_api

        self.route_id = route_id
        self.direction_name = direction_name
        self.stop_id = stop_id
        self.stop_name = stop_name

        self.predictions = None

    def load_predictions(self):
        resp = self.mbta_api.get_predictions(
            route_id=self.route_id, stop_id=self.stop_id
        )

        self.predictions = []
        for p in resp:
            arrival_time = p["attributes"]["arrival_time"]
            t = datetime.strptime(arrival_time, "%Y-%m-%dT%H:%M:%S.%f%z")
            self.predictions.append(t)

