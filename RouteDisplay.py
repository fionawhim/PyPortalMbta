import gc

from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

HELVETICA_16 = bitmap_font.load_font("/fonts/Helvetica-16.bdf")
HELVETICA_16.load_glyphs(b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') # pre-load glyphs for fast printing

HELVETICA_50 = bitmap_font.load_font("/fonts/Helvetica-Bold-50.bdf")
HELVETICA_50.load_glyphs(b'0123456789') # pre-load glyphs for fast printing

gc.collect()

X_PADDING = 15
Y_PADDING = 30

ROW_HEIGHT = 80

class RouteDisplay:
    def __init__(self, group, stop, i):
        self.stop = stop

        self.route_label = label.Label(HELVETICA_50, max_glyphs=3)
        self.route_label.x = X_PADDING 
        self.route_label.y = Y_PADDING + ROW_HEIGHT * i

        self.direction_label = label.Label(HELVETICA_16, max_glyphs=48, color=0x666666)
        self.direction_label.x = X_PADDING
        self.direction_label.y = Y_PADDING + 35 + ROW_HEIGHT * i

        group.append(self.route_label)
        group.append(self.direction_label)

    def render(self):
        self.route_label.text = self.stop.route_id 
        self.direction_label.text = self.stop.direction_name[:48]

