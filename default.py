import xbmc
from resources.lib.addon import Addon
from resources.lib.data import Data
from PIL import ImageGrab
import random

import xbmcgui

class Script:
    def __init__(self):
        self.data = Data()
        pass

    def main(self):

        capture = xbmc.RenderCapture()

        xbmc.log('START', level=-1)

        xbmc.log("aspect", level=-1)
        xbmc.log(str(capture.getAspectRatio()), level=-1)

        image = ImageGrab.grab()
        total_width, height = image.size

        xbmc.log('width', level=-1)
        xbmc.log(str(total_width), level=-1)
        width = int(height * capture.getAspectRatio())

        xbmc.log(str(int(width)), level=-1)

        # use capture.getAspectRatio()
        aspect = str(xbmc.getInfoLabel('VideoPlayer.VideoAspect'))
        xbmc.log(str(aspect), level=-1)

        # box size
        box_size_x = width / 100
        box_size_y = height / 100

        xbmc.log("box_size", level=-1)
        xbmc.log(str(box_size_x), level=-1)
        xbmc.log(str(box_size_y), level=-1)

        # box position
        area_min_x = (total_width - width) / 2
        area_max_x = total_width - area_min_x - box_size_x
        area_max_y = height / 10 - box_size_y

        xbmc.log("area_", level=-1)
        xbmc.log(str(area_min_x), level=-1)
        xbmc.log(str(area_max_x), level=-1)
        xbmc.log(str(area_max_y), level=-1)

        box_start_x, box_start_y = Script().get_box_start( area_min_x, area_max_x, area_max_y)

        #box_start_x = random.randint(area_min_x, area_max_x)
        #box_start_y = random.randint(5, area_max_y)

        xbmc.log("ramnd", level=-1)
        xbmc.log(str(box_start_x) + ' ' + str(box_start_y), level=-1)

        black = Script().get_black(image, box_start_x, box_start_y, box_size_x, box_size_y)

        if black:
            dialog = xbmcgui.Dialog()
            dialog.notification('OUTRO', 'BLACK', xbmcgui.NOTIFICATION_INFO, 1000)
            xbmc.log("REAL BLACK")


    def get_box_start(self, area_min_x, area_max_x, area_max_y):
        box_start_x = random.randint(area_min_x, area_max_x)
        box_start_y = random.randint(5, area_max_y)

        return box_start_x, box_start_y


    def get_black(self, image, box_start_x, box_start_y, box_size_x, box_size_y):
        black = True
        for i in range(1, 10, 1):
            x = random.randint(box_start_x, box_start_x + box_size_x)
            y = random.randint(box_start_y, box_start_y + box_size_y)

            color = image.getpixel((x, y))

            if color[0] > 10 or color[1] > 10 or color[2] > 10:
                black = False
            xbmc.log("clear")
            if black:
                xbmc.log("BLACK")
            else:
                xbmc.log("NOT BLACK")

        return black


    def get_tenth(self, width, height):
        rel_height = int(height * 0.1)
        rel_width = int(width * 0.1)

        return rel_width, rel_height

    def rgb2hex(self, r, g, b):
        # https://stackoverflow.com/questions/3380726/converting-a-rgb-color-tuple-to-a-six-digit-code-in-python
        hex = "#{:02x}{:02x}{:02x}".format(r, g, b)

        return hex

if __name__ == "__main__":
    Script().main()
