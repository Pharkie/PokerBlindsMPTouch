# round.py Test/demo program for micropython-touch plot. Cross-patform,

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2021-2024 Peter Hinch

# Create SSD instance. Must be done first because of RAM use.
import hardware_setup
from machine import Timer
import time

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
        print(f"SSD dimensions: {ssd.width} x {ssd.height}")
        fn = "mylogo8bit.bin"  # Image created by `img_cvt.py`

        try:
            with open(fn, "rb") as f:
                rows = int.from_bytes(f.read(2), "big")
                cols = int.from_bytes(f.read(2), "big")

            print(f"Image size: {rows} rows x {cols} cols")

            with open(fn, "rb") as f:
                _ = f.read(4)  # Discard first 4 bytes (rows and cols)
                f.readinto(ssd.mvb)  # Read the image into the frame buffer

            ssd.show()  # Refresh the display to show the new image

        except OSError as e:
            print(f"Failed to open file {fn}: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        print("Logo displayed")
        time.sleep(2)
        Screen.change(BaseScreen, mode=Screen.REPLACE)


class BaseScreen(Screen):
    def __init__(self):
        super().__init__()
        pad = Pad(wri, 0, 0, height=239, width=239, callback=self.cb)
        col = 40
        l = Label(wri, 100, col, "Poker blinds", fgcolor=RED)
        l = Label(
            wri, l.mrow + 2, col, "Touch screen to start timer", fgcolor=CYAN
        )

    def cb(self, _):  # Change to LogoScreen
        Screen.change(CountdownScreen, mode=Screen.REPLACE)


class CountdownScreen(Screen):
    def __init__(self):
        super().__init__()
        self.remaining_time = 10 * 60  # 10 minutes in seconds
        self.timer = Timer(-1)
        self.update_display()  # Display initial time
        self.start_timer()  # Start the timer

    def update_display(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        time_str = f"{minutes:02}:{seconds:02}"
        Label(wri, 100, 100, time_str, fgcolor=WHITE)

    def start_timer(self):
        self.timer.init(period=1000, mode=Timer.PERIODIC, callback=self.tick)

    def tick(self, timer):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_display()
        else:
            self.timer.deinit()
            Screen.back()

    def cb(self, _):  # Change to LogoScreen
        Screen.back()


def main():
    print("Starting program")

    Screen.change(LogoScreen)  # Load the logo


main()
