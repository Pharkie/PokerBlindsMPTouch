# round.py Test/demo program for micropython-touch plot. Cross-patform,

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2021-2024 Peter Hinch

# Create SSD instance. Must be done first because of RAM use.
import hardware_setup

from gui.core.writer import CWriter
from gui.core.tgui import Screen, ssd
from gui.widgets import Pad, Label

# import mylogo  # Python file containing the image

# Fonts & colors
import gui.fonts.font10 as font
from gui.core.colors import *

wri = CWriter(ssd, font, GREEN, BLACK)


class LogoScreen(Screen):
    def __init__(self):
        super().__init__()

    def after_open(self):
        # print(f"SSD dimensions: {ssd.width} x {ssd.height}")
        fn = "mylogo8bit.bin"  # Image created by `img_cvt.py`

        try:
            with open(fn, "rb") as f:
                rows = int.from_bytes(f.read(2), "big")
                cols = int.from_bytes(f.read(2), "big")

            # print(f"Image size: {rows} rows x {cols} cols")

            with open(fn, "rb") as f:
                _ = f.read(4)  # Discard first 4 bytes (rows and cols)
                f.readinto(ssd.mvb)  # Read the image into the frame buffer

            ssd.show()  # Refresh the display to show the new image

        except OSError as e:
            print(f"Failed to open file {fn}: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


class BaseScreen(Screen):
    def __init__(self):
        super().__init__()
        pad = Pad(wri, 0, 0, height=239, width=239, callback=self.cb)
        col = 40
        l = Label(wri, 100, col, "Logo demo", fgcolor=RED)
        l = Label(
            wri, l.mrow + 2, col, "Touch screen to load logo", fgcolor=CYAN
        )

    def cb(self, _):  # Change to LogoScreen
        Screen.change(LogoScreen, mode=Screen.REPLACE)


def main():
    print("Starting program")

    Screen.change(BaseScreen)


main()
