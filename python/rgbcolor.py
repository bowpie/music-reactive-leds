import colorsys
import ast
from config import COLORS_PATH
import logging
import json


class RgbColor:
    logger = logging.getLogger(__name__)

    def __init__(self, rgb: tuple = None, name: str = None, hsv: tuple = None):
        if name:
            rgb = self.rgb_from_name(name)
        else:
            if rgb:
                rgb = self.rgb_from_code(rgb)
            if hsv:
                rgb = self.rgb_from_hsv(hsv)
                self.hsv = hsv

        self.rgb = tuple([RgbColor.constrain(int(e), 0, 255) for e in rgb])
        if not hsv:
            self.hsv = self.hsv_from_rgb(self.rgb)
        self.color_dict = json.load(open(COLORS_PATH, "r"))

    def __str__(self):
        # r, g, b = self.rgb
        h, s, v = self.hsv
        return f"hsv<{h}, {s}, {v}>"

    def __repr__(self):
        return self.__str__()

    def rgb_from_name(self, name: str):
        return tuple(int(e) for e in ast.literal_eval(self.find_color(name)["rgb"]))

    def rgb_from_code(self, code: tuple):
        return code

    def rgb_from_hsv(self, hsv: tuple):
        h, s, v = hsv
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h / 360, s, v))

    def hsv_from_rgb(self, rgb: tuple):
        r, g, b = rgb
        hsv = [e for e in colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)]
        hsv[0] *= 360
        return tuple(hsv)

    def power(self, percentage: float):
        h, s, v = self.hsv
        return RgbColor(hsv=(h, s, percentage / 100))

    def find_color(self, name: str):
        try:
            return self.color_dict[name]
        except KeyError:
            RgbColor.logger.error("Color not found. Defaulting to red.")
            return RgbColor(rgb=(255, 0, 0))

    @staticmethod
    def constrain(val, min_val, max_val):
        return min(max_val, max(min_val, val))
