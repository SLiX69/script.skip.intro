import xbmc
import time
from resources.lib.data import Data
from resources.lib.addon import Addon
import difflib
from PIL import ImageGrab
import random
import math

import xbmcgui


class MyPlayer(xbmc.Player):

    paused = False
    # TODO: Stop Service if video was already skipped

    def __init__(self):
        pass

    def onPlayBackResumed(self):
        self.onPlayBackStarted()

    def onPlayBackPaused(self):
        self.paused = True

    def onPlayBackStarted(self):
        self.paused = False

        if sc.serv:
            monitor = xbmc.Monitor()
            while not monitor.abortRequested() and xbmc.Player().isPlayingVideo() and not self.paused:
                # Sleep/wait for abort for 5 seconds
                sc.main()
                if monitor.waitForAbort(3):
                    # Abort was requested while waiting. We should exit
                    break


class Service:
    serv = False
    intr_serv = False
    outr_static_serv = False
    outr_auto_serv = False
    outr_auto_shows_only = True

    def __init__(self):
        self.ad = Addon()
        self.data = Data()
        self.intr_serv = self.ad.get_state_intro_service()
        self.outr_static_serv = self.ad.get_state_outro_static_service()
        self.outr_auto_serv = self.ad.get_state_outro_auto_service()
        self.outr_auto_shows_only = self.ad.get_state_outro_auto_service_shows_only()

        if self.intr_serv or self.outr_static_serv or self.outr_auto_serv:
            self.serv = True


    def main(self):
        dialog = xbmcgui.Dialog()
        #dialog.notification('Service', 'STARTED', xbmcgui.NOTIFICATION_INFO, 3000)
        xbmc.log("PRINT", level=-1)
        xbmc.log(str(self.intr_serv))
        try:
            # TODO if obsolete
            # is only called when playing
            if xbmc.Player().isPlaying():
                xbmc.log("PLAYING", level=-1)
                cur_time = xbmc.Player().getTime()
                cur_title = xbmc.Player().getVideoInfoTag().getTVShowTitle()

                if self.intr_serv:
                    if cur_time < 10:
                        for show in self.data.tdata:

                            dis = difflib.SequenceMatcher(None, cur_title, show['title']).ratio()
                            # if cur_title == show["title"]: ## OLD

                            if dis >= 0.9:
                                seek_time = show["introLength"]
                                xbmc.Player().seekTime(seek_time)
                                xbmc.sleep(10000)

                                xbmc.log("SKIPPED", level=-1)
                                # found show, exit loop
                                break

                # SKIP OUTRO
                if self.outr_auto_serv or self.outr_static_serv:
                    tot_time = xbmc.Player().getTotalTime()
                    if tot_time * 0.9 <= cur_time:

                        # Calling STATIC outro service
                        if self.outr_static_serv:
                            for show in self.data.tdata:
                                dis = difflib.SequenceMatcher(None, cur_title, show['title']).ratio()
                                if dis >= 0.9:
                                    outro_length = show["outroLength"]

                                    xbmc.log("OUTRO-LENGTH", level=-1)
                                    xbmc.log(str(outro_length), level=-1)

                                    #if tot_time - outro_length >= cur_time:
                                    if cur_time >= tot_time - outro_length:
                                        xbmc.log(str(tot_time), level=-1)
                                        xbmc.log(str(outro_length), level=-1)
                                        xbmc.log(str(cur_time), level=-1)
                                        dialog = xbmcgui.Dialog()
                                        dialog.notification('SKIPPED!!', '7070', xbmcgui.NOTIFICATION_INFO, 1000)
                                        xbmc.Player().playnext()
                                        # found show, exit loop
                                        break

                        # Calling AUTO outro service
                        if self.outr_auto_serv:
                            # check if tv-show is playing (no movie, video-addon, etc)
                            if self.outr_auto_shows_only:
                                if cur_title != "":
                                    Outro().main()
                            else:
                                Outro().main()

            else:
                # not playing
                xbmc.log("NOT PLAYING", level=-1)

        except Exception as e:
            xbmc.log("EXCEPTION", level=-1)
            xbmc.log(str(e), level=-1)
            pass


class Outro:

    def __init__(self):
        pass

    def main(self):

        skip = False

        capture = xbmc.RenderCapture()

        image = ImageGrab.grab()
        total_width, height = image.size

        width = int(height * capture.getAspectRatio())

        # use capture.getAspectRatio()
        aspect = str(xbmc.getInfoLabel('VideoPlayer.VideoAspect'))
        xbmc.log(str(aspect), level=-1)

        width_list = [0.25, 0.5, 0.75]
        list = []

        for j in width_list:

            vid_height = height
            vid_width = width

            # get perc. x-ord (1/4, 1/2, 3/4)
            box_start_x = int(vid_width * j)
            box_start_y = int(vid_height * 0.1)

            box_size_x = int(math.fabs(float(j) * 100))
            box_size_y = box_size_x

            list.append(
                {
                    'name': 'box',
                    'sc_height': vid_height,
                    'sc_width': vid_width,
                    'box_start_x': box_start_x,
                    'box_start_y': box_start_y,
                    'box_size_x': box_size_x,
                    'box_size_y': box_size_y
                }
            )
        # endfor

        cnt_black = 0
        cnt_box = 0

        for box in list:
            cnt_box += 1
            xbmc.log("BOX: " + str(cnt_box), level=-1)

            box_start_x = box['box_start_x']
            box_start_y = box['box_start_y']
            box_size_x = box['box_size_x']
            box_size_y = box['box_size_y']

            black = Outro().get_black(image, box_start_x, box_start_y, box_size_x, box_size_y)

            xbmc.log("test: " + str(box_start_x) + ' ' + str(box_start_y) + ' ' + str(box_size_x) + ' ' + str(box_size_y) + ' ' + str(black),
                     level=-1)

            if black:
                cnt_black += 1
            else:
                # got non-black pixel, break loop, this is not the outro
                break

        if cnt_black == len(list):
            # only got black pixels from (three) boxes, let's check again
            cnt_black = 0

            dialog.notification('OUTRO', 'BLACK-1', xbmcgui.NOTIFICATION_INFO, 1000)
            xbmc.sleep(3000)
            # grab image
            image = ImageGrab.grab()

            for box in list:

                box_start_x = box['box_start_x']
                box_start_y = box['box_start_y']
                box_size_x = box['box_size_x']
                box_size_y = box['box_size_y']

                black = Outro().get_black(image, box_start_x, box_start_y, box_size_x, box_size_y)

                xbmc.log("test_b2: " + str(box_start_x) + ' ' + str(box_start_y) + ' ' + str(box_size_x) + ' ' + str(
                    box_size_y) + ' ' + str(black),
                         level=-1)

                if black:
                    cnt_black += 1
                else:
                    # got non black pixel, exit loop, this is not the outro
                    break
            # endfor

            if cnt_black == len(list):

                cnt_black = 0

                dialog.notification('OUTRO', 'BLACK-2', xbmcgui.NOTIFICATION_INFO, 1000)
                xbmc.sleep(3000)
                # grab image
                image = ImageGrab.grab()

                for box in list:

                    box_start_x = box['box_start_x']
                    box_start_y = box['box_start_y']
                    box_size_x = box['box_size_x']
                    box_size_y = box['box_size_y']

                    black = Outro().get_black(image, box_start_x, box_start_y, box_size_x, box_size_y)

                    xbmc.log("test_b3: " + str(box_start_x) + ' ' + str(box_start_y) + ' ' + str(box_size_x) + ' ' + str(
                        box_size_y) + ' ' + str(black),
                             level=-1)

                    if black:
                        cnt_black += 1
                    else:
                        # got non black pixel, exit loop, this is not the outro
                        break

                if cnt_black == len(list):
                    # just black pixels, this must be the outro
                    skip = True

        else:
            # dialog.notification('OUTRO', 'FOUND COLORED PIXEL in vorgang 1', xbmcgui.NOTIFICATION_INFO, 100)
            # return because found colored pixel in a box
            return

        if skip:
            xbmc.Player().playnext()



    def get_black(self, image, box_start_x, box_start_y, box_size_x, box_size_y):
        xbmc.log("GET-BLACK: " + str(box_start_x) + ' ' + str(box_start_y) + ' ' + str(box_size_x) + ' ' + str(box_size_y), level=-1)
        black = True

        for i in range(1, 10, 1):
            x = random.randint(box_start_x, box_start_x + box_size_x)
            y = random.randint(box_start_y, box_start_y + box_size_y)

            color = image.getpixel((x, y))

            if color[0] > 10 or color[1] > 10 or color[2] > 10:
                black = False

        return black


if __name__ == "__main__":
    sc = Service()
    player = MyPlayer()
    dialog = xbmcgui.Dialog()
    dialog.notification('INIT', 'init', xbmcgui.NOTIFICATION_INFO, 1000)
    if Service().serv:
        monitor = xbmc.Monitor()
        while not monitor.abortRequested():
            # Sleep/wait for abort for 5 seconds
            if monitor.waitForAbort(5):
                # Abort was requested while waiting. We should exit
                break
            pass
