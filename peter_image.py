import hardware_setup
from gui.core.tgui import Screen, ssd

from gui.widgets import Label, Button, CloseButton
from gui.core.writer import CWriter
import gui.fonts.freesans20 as font
from gui.core.colors import *
import time
import os


class BaseScreen(Screen):
    def __init__(self):
        super().__init__()
        wri = CWriter(ssd, font, GREEN, BLACK)  # Clears screen
        col = 2
        row = 120
        Label(wri, row, col, "Simple Demo")
        print("Waiting")
        CloseButton(wri, 30)  # Quit the application

    def after_open(self):
        print("Showing image")
        file_path = "optional/bitmaps/m00"
        try:
            with open(file_path, "rb") as f:
                f.read(4)
                f.readinto(ssd.mvb)
        except OSError as e:
            print(f"Error reading file: {e}")


def test():
    Screen.change(BaseScreen)


test()
