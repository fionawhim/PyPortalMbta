import time
import board
import busio
from digitalio import DigitalInOut
import neopixel
import displayio
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager

from MbtaApi import MbtaApi, MbtaApiFake
from Stop import Stop
from RouteDisplay import RouteDisplay

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
status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

LAT = 42.37
LNG = -71.0844

# mbta_api = MbtaApi(wifi, lat=LAT, lng=LNG)
mbta_api = MbtaApiFake()

ROUTES = [("69", 0), ("87", 0), ("88", 0)]

STOPS = []
DISPLAYS = []

TEST_TIME = "2019-05-03T23:24:00+0000"
TEST_TIME_EPOCH = 1556925840

group = displayio.Group(max_size=15)
board.DISPLAY.show(group)


def startup():
    for i, (r, direction) in enumerate(ROUTES):
        stop, route = mbta_api.get_nearest_stop(r, direction)

        s = Stop(
            mbta_api=mbta_api,
            route_id=route["id"],
            direction_name=route["attributes"]["direction_destinations"][direction],
            stop_id=stop["id"],
            stop_name=stop["attributes"]["name"],
        )

        STOPS.append(s)
        DISPLAYS.append(RouteDisplay(group=group, stop=s, i=i))

    for s in STOPS:
        s.load_predictions()

    for s in STOPS:
        print(s.route_id, s.stop_name)

        for t in s.predictions:
            print(t)

        print()


startup()

while True:
    for d in DISPLAYS:
        d.render()

    board.DISPLAY.refresh_soon()
    board.DISPLAY.wait_for_frame()
    time.sleep(10)


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
