import time
import board
import busio
import re
from digitalio import DigitalInOut
import neopixel
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager

from url_helpers import make_q, URL_BASE
from stop import Stop

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
status_light = neopixel.NeoPixel(
    board.NEOPIXEL, 1, brightness=0.2
) 
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

LAT = 42.37
LNG = -71.0844


ROUTES = [("69", 0), ("87", 0)]  # , ("88", 0)]


def get_nearest_stop(wifi, route, direction_id):
    stops_url = (
        URL_BASE
        + "stops?"
        + make_q(
            {
                "page[limit]": 1,
                "sort": "distance",
                "include": "route",
                "filter[route]": route,
                "filter[direction_id]": direction_id,
                "filter[latitude]": LAT,
                "filter[longitude]": LNG,
            }
        )
    )

    response = wifi.get(stops_url)
    response_json = response.json()

    stop = response_json["data"][0]
    route = response_json["included"][0]

    response.close()

    return (stop, route)



STOPS = []

def startup():
    for (r, direction) in ROUTES:
        stop, route = get_nearest_stop(wifi, r, direction)
        STOPS.append(
            Stop(
                route_id=route["id"],
                stop_id=stop["id"],
                stop_name=stop["attributes"]["name"],
            )
        )

    for s in STOPS:
        s.load_predictions(wifi)

    for s in STOPS:
        print(s.route_id, s.stop_name)

        for t in s.predictions:
            print(t)

        print()

startup()


# while True:
#     try:
#         print("Posting data...", end='')
#         data = counter
#         feed = 'test'
#         payload = {'value':data}
#         response = wifi.post(
#             "https://io.adafruit.com/api/v2/"+secrets['aio_username']+"/feeds/"+feed+"/data",
#             json=payload,
#             headers={"X-AIO-KEY":secrets['aio_key']})
#         print(response.json())
#         response.close()
#         counter = counter + 1
#         print("OK")
#     except (ValueError, RuntimeError) as e:
#         print("Failed to get data, retrying\n", e)
#         wifi.reset()
#         continue
#     response = None
#     time.sleep(15)
