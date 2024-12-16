import time
from machine import Pin
import neopixel

# Configuration
LED_PIN = 17  # GPIO pin connected to D0
NUM_LEDS = 12  # Number of LEDs in the ring
TRAIL_LENGTH = 12  # Number of LEDs in the trail
FLASH_COLOR = (0, 255, 0)  # Green color for flashing
FLASH_DURATION = 3  # Flash duration in seconds


# Function to create a trailing fade effect with configurable trail length
def spin_with_trail():
    for i in range(NUM_LEDS):
        for j in range(NUM_LEDS):
            if j == i:
                np[j] = (0, 0, 255)  # Blue
            elif 0 < (i - j) <= TRAIL_LENGTH:
                np[j] = (
                    0,
                    0,
                    int(255 * (TRAIL_LENGTH - (i - j)) / TRAIL_LENGTH),
                )  # Fade effect
            else:
                np[j] = (0, 0, 0)  # Turn off
        np.write()
        time.sleep(1 / NUM_LEDS)


# Function to fade each LED in turn to off
def fade_out():
    for i in range(NUM_LEDS):
        for j in range(NUM_LEDS):
            if j == i:
                np[j] = (0, 0, 0)  # Turn off
            else:
                np[j] = np[j]  # Keep current color
        np.write()
        time.sleep(1 / NUM_LEDS)


# Function to flash all LEDs with a specific color once per second
def flash_all(color, duration):
    end_time = time.time() + duration
    step = 5  # Step size for brightness change
    while time.time() < end_time:
        # Fade up to full brightness
        for brightness in range(0, 256, step):
            for i in range(NUM_LEDS):
                np[i] = (
                    color[0] * brightness // 255,
                    color[1] * brightness // 255,
                    color[2] * brightness // 255,
                )
            np.write()
            time.sleep(0.01)
        # Fade down to off
        for brightness in range(255, -1, -step):
            for i in range(NUM_LEDS):
                np[i] = (
                    color[0] * brightness // 255,
                    color[1] * brightness // 255,
                    color[2] * brightness // 255,
                )
            np.write()
            time.sleep(0.01)


# Function to create a fun startup effect with a color-changing trail
def startup_effect():
    def wheel(pos):
        # Input a value 0 to 255 to get a color value.
        # The colors are a transition r - g - b - back to r.
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        else:
            pos -= 170
            return (pos * 3, 0, 255 - pos * 3)

    for cycle in range(3):  # Run 3 cycles
        for i in range(NUM_LEDS):
            for j in range(NUM_LEDS):
                if j == i:
                    np[j] = wheel((i * 256 // NUM_LEDS) & 255)  # Change color
                elif 0 < (i - j) <= TRAIL_LENGTH:
                    color = wheel((i * 256 // NUM_LEDS) & 255)
                    np[j] = (
                        color[0] * (TRAIL_LENGTH - (i - j)) // TRAIL_LENGTH,
                        color[1] * (TRAIL_LENGTH - (i - j)) // TRAIL_LENGTH,
                        color[2] * (TRAIL_LENGTH - (i - j)) // TRAIL_LENGTH,
                    )  # Fade effect
                else:
                    np[j] = (0, 0, 0)  # Turn off
            np.write()
            time.sleep(0.1)
        # Fade to new color
        for brightness in range(255, -1, -5):
            for i in range(NUM_LEDS):
                color = wheel((cycle * 85) & 255)
                np[i] = (
                    color[0] * brightness // 255,
                    color[1] * brightness // 255,
                    color[2] * brightness // 255,
                )
            np.write()
            time.sleep(0.01)
    # Fade to off from current color
    for brightness in range(255, -1, -5):
        for i in range(NUM_LEDS):
            color = np[i]
            np[i] = (
                color[0] * brightness // 255,
                color[1] * brightness // 255,
                color[2] * brightness // 255,
            )
        np.write()
        time.sleep(0.01)
    time.sleep(3)  # Wait 3 seconds


np = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS)

# Example: Animate LEDs with trailing fade effect, fade out effect, and flash effect
startup_effect()  # Play startup effect once
while True:
    for _ in range(3):  # Complete 3 circles
        spin_with_trail()
        fade_out()
    flash_all(FLASH_COLOR, FLASH_DURATION)  # Flash all LEDs
