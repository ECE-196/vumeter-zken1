import board
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
from time import sleep

# setup pins
microphone = AnalogIn(board.IO1)

status = DigitalInOut(board.IO17)
status.direction = Direction.OUTPUT

# Configure LED pins
led_pins = [
    board.IO21,
    board.IO26,  
    board.IO47,
    board.IO33,
    board.IO34,
    board.IO48,
    board.IO35,
    board.IO36,
    board.IO37,
    board.IO38,
    board.IO39,
]

# gives status of each LED in a list
leds = [DigitalInOut(pin) for pin in led_pins]  

# all led in leds are output values 
for led in leds:
    led.direction = Direction.OUTPUT

# Define range for microphone
MIN_VOLUME = 20000
MAX_VOLUME = 48000

# Define filter parameters
FILTER_CONSTANT = 0.5  # Adjust this value to control the speed of decay

# Initialize filtered volume
filtered_volume = 0

# Main loop
while True:
    volume = microphone.value

    # Scale the volume value to the range 0 to 1
    scaled_volume = (volume - MIN_VOLUME) / (MAX_VOLUME - MIN_VOLUME)
    scaled_volume = max(0, min(1, scaled_volume))  

    # Apply low-pass filter to the volume: simple exponential smoothing algorithm [https://www.getcensus.com/blog/predicting-the-future-time-series-analysis-with-simple-exponential-smoothing]
    filtered_volume = filtered_volume * (1 - FILTER_CONSTANT) + scaled_volume * FILTER_CONSTANT

    # Calculate the LED level based on the filtered volume level
    led_level = round(filtered_volume * len(leds))

    # Turn on LEDs up to the calculated LED level
    for i in range(len(leds)):
        leds[i].value = i < led_level

    # Debugging
    # print(volume)
    # print(scaled_volume, "S")
    # print(filtered_volume,  "F")
    # print(led_level)

    sleep(0.05)  # Adjust this delay as needed for smoother animation
