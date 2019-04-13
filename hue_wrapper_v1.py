import time
from random import randint

import requests

from hue_wrapper import HueWrapperBase
from huepythonrgbconverter.rgbxy import Converter, GamutC


class HueWrapperV1(HueWrapperBase):
    """
    An first wrapper implementation most important functions for interacting
    with the phillips hue smart lightbulbs
    """

    def __init__(self):
        """
        initialize persistent information and reset lamp
        """

        # read in url
        config_file = open("data.cfg", "r")
        if config_file.mode == 'r':
            config_file_lines = config_file.readlines()
            self.bridge_ip = config_file_lines[0][0:-1]
            self.usr_name = config_file_lines[1][0:-1]
        else:
            print("ERROR: config file not found.")
            exit()
        self.url = self.bridge_ip + self.usr_name + '/lights/1/state'
        self.headers = {'Authorization': 'Bearer pGMBx9NF9SZXprHb6ZbJ86zN0PMV',
                        'Content-Type': 'application/json'}

        # set rgb Converter
        self.converter = Converter(GamutC)

        # reset lamp
        self.set_mode(0)
        time.sleep(0.5)

    def _send_command(self, url, data):
        """
        send specific command to lamp

        Arguments
        ---------
        url (string): the url
        data (string): the data in json format

        Returns
        -------
        void
        """
        data = data[0:-1] + ', "bri":255, "transitiontime":0}'
        requests.put(url, data=data, headers=self.headers)

    def set_mode(self, mode):
        """
        set lamp in a specific mode. available modes are
            0 - off
            1 - on
            2 - color cycle

        Arguments
        ---------
        mode (int): the mode, see modes above

        Returns
        -------
        void
        """
        if mode == 0:
            data = '{"on":false}'
            self.state = 0
        elif mode == 1:
            data = '{"on":true}'
            self.state = 1
        elif mode == 2:
            data = '{"effect":"colorloop"}'
        else:
            print("Warning: No mode selected.")
            return
        self._send_command(self.url, data)

    def set_color(self, r, g, b):
        """
        set the color to a rgb color

        Arguments
        ---------
        r (int): red value of color between 0 and 255
        g (int): green value of color between 0 and 255
        b (int): blue value of color between 0 and 255

        Returns
        -------
        void
        """
        xy = self.converter.rgb_to_xy(r, g, b)
        data = '{"on":true, "xy":[' + str(xy)[1:-1] + ']}'
        self._send_command(self.url, data)

    def toggle_on_off(self):
        """
        switch the hue on if it is off and vice versa

        Arguments
        ---------
        void

        Returns
        -------
        void
        """
        if self.state:
            self.set_mode(0)
        else:
            self.set_mode(1)

    def blink(self, r, g, b, freq, dur):
        """
        set lamp in a specific dance mode. available modes are
            0 - random
            1 - rgb
            2 - rgbmcy

        Arguments
        ---------
        r (int): red value of color between 0 and 255
        g (int): green value of color between 0 and 255
        b (int): blue value of color between 0 and 255
        freq (double): blinking frequency
        dur (int): blinking duration

        Returns
        -------
        void
        """

        # turn on for clean start
        self.set_color(r, g, b)
        time.sleep(1.0 / freq)

        # run blinking loop
        for i in range(0, int(dur * freq - 1)):
            self.toggle_on_off()
            time.sleep(1.0 / freq)

    def dance(self, mode, freq, dur):
        """
        set lamp in a specific dance mode. available modes are
            0 - random
            1 - rgb
            2 - rgbmcy

        Arguments
        ---------
        mode (int): the mode, see modes above
        freq (double): blinking frequency
        dur (int): blinking duration

        Returns
        -------
        void
        """

        if mode == 0:
            # run blinking loop
            for i in range(0, int(dur * freq)):
                self.set_color(randint(0, 255), randint(
                    0, 255), randint(0, 255))
                time.sleep(1.0 / freq)

        elif mode == 1:
            # run blinking loop
            for i in range(0, int(dur * freq / 3)):
                self.set_color(0, 255, 0)
                time.sleep(1.0 / freq)
                self.set_color(0, 0, 255)
                time.sleep(1.0 / freq)
                self.set_color(255, 0, 0)
                time.sleep(1.0 / freq)

        elif mode == 2:
            # run blinking loop
            for i in range(0, int(dur * freq / 6)):
                self.set_color(255, 255, 0)
                time.sleep(1.0 / freq)
                self.set_color(0, 255, 0)
                time.sleep(1.0 / freq)
                self.set_color(0, 255, 255)
                time.sleep(1.0 / freq)
                self.set_color(0, 0, 255)
                time.sleep(1.0 / freq)
                self.set_color(255, 0, 255)
                time.sleep(1.0 / freq)
                self.set_color(255, 0, 0)
                time.sleep(1.0 / freq)

        else:
            print("Warning: No mode selected.")
            return
