# round.py Test/demo program for micropython-touch plot. Cross-patform,

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2021-2024 Peter Hinch

# Create SSD instance. Must be done first because of RAM use.
import hardware_setup

from gui.core.writer import CWriter
from gui.core.tgui import Screen, ssd
from gui.widgets import Pad, Label
import mylogo  # Python file containing the image

# Fonts & colors
import gui.fonts.font10 as font
from gui.core.colors import *

wri = CWriter(ssd, font, GREEN, BLACK)


# class LogoScreen(Screen):
#     def __init__(self):
#         super().__init__()

#     def after_open(self):
#         fn = "mylogo.bin"  # Image created by`img_cvt.py`

#         with open(fn, "rb") as f:
#             rows = int.from_bytes(f.read(2), "big")
#             cols = int.from_bytes(f.read(2), "big")

#         print(f"Image size: {rows} rows x {cols} cols")

#         with open(fn, "rb") as f:
#             _ = f.read(4)  # Read and discard rows and cols
#             f.readinto(ssd.mvb)  # Read the image into the frame buffer


# class LogoScreen(Screen):
#     def __init__(self):
#         super().__init__()

#     def after_open(self):
#         print(f"SSD dimensions: {ssd.width} x {ssd.height}")
#         fn = "mylogo.bin"  # Image created by`img_cvt.py`

#         with open(fn, "rb") as f:
#             rows = int.from_bytes(f.read(2), "big")
#             cols = int.from_bytes(f.read(2), "big")

#         print(f"Image size: {rows} rows x {cols} cols")

#         with open(fn, "rb") as f:
#             _ = f.read(4)  # Discard first 4 bytes (rows and cols)
#             image_data = f.read(rows * cols)  # Read the image data

#         # Ensure the image data fits into the display buffer
#         print(f"Image data size: {len(image_data)}")

#         if len(image_data) != rows * cols:
#             raise ValueError(
#                 "Image data size does not match expected dimensions"
#             )

#         # Copy image data into the display buffer
#         for row in range(rows):
#             for col in range(cols):
#                 if row < ssd.height and col < ssd.width:
#                     index = row * cols + col
#                     ssd_index = row * ssd.width + col
#                     # print(
#                     #     f"row: {row}, col: {col}"
#                     # )
#                     if ssd_index < len(ssd.mvb):
#                         ssd.mvb[ssd_index] = image_data[index]

#         ssd.show()  # Refresh the display to show the new image


# class BaseScreen(Screen):
#     def __init__(self):
#         super().__init__()
#         pad = Pad(wri, 0, 0, height=239, width=239, callback=self.cb)
#         col = 40
#         l = Label(wri, 100, col, "Logo demo", fgcolor=RED)
#         l = Label(
#             wri, l.mrow + 2, col, "Touch screen to load logo", fgcolor=CYAN
#         )

#     def cb(self, _):  # Change to LogoScreen
#         Screen.change(LogoScreen, mode=Screen.REPLACE)


def main():
    print("Starting program")

    print(f"SSD dimensions: {ssd.width} x {ssd.height}")
    print(f"Image size: {mylogo.rows} rows x {mylogo.cols} cols")

    # Ensure the image data fits into the display buffer
    if len(mylogo.data) != mylogo.rows * mylogo.cols:
        print(
            f"Image data size: {len(mylogo.data)} and expected size: {mylogo.rows * mylogo.cols}"
        )
        raise ValueError("Image data size does not match expected dimensions")

    # Ensure the display buffer is correctly sized
    if len(ssd.mvb) != ssd.width * ssd.height:
        print(
            f"Display buffer size: {len(ssd.mvb)} and expected size: {ssd.width * ssd.height}"
        )
        raise ValueError(
            "Display buffer size does not match display dimensions"
        )

    # Copy image data into the display buffer
    for row in range(mylogo.rows):
        for col in range(mylogo.cols):
            if row < ssd.height and col < ssd.width:
                index = row * mylogo.cols + col
                ssd_index = row * ssd.width + col
                try:
                    ssd.mvb[ssd_index] = mylogo.data[index]
                except IndexError:
                    print(
                        f"IndexError at row: {row}, col: {col}, ssd_index: {ssd_index}"
                    )
                    raise

    ssd.show()  # Refresh the display to show the new image


main()

# def main():
#     print("Starting program")

#     print(f"SSD dimensions: {ssd.width} x {ssd.height}")
#     print(f"Image size: {mylogo.rows} rows x {mylogo.cols} cols")

#     # ssd.mvb[:] = mylogo.data

#     # Ensure the image data fits into the display buffer
#     if len(mylogo.data) != len(ssd.mvb):
#         print(
#             f"Image data size: {len(mylogo.data)} and SSD data: {len(ssd.mvb)}"
#         )
#         raise ValueError("Image data size does not match display buffer size")

#     # Copy image data into the display buffer
#     for i in range(len(mylogo.data)):
#         ssd.mvb[i] = mylogo.data[i]

#     # Screen.change(BaseScreen)


# main()
