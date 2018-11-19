from machine import Pin


ON = 0
OFF = 1

LED = Pin(2, Pin.OUT)
BUTTON = Pin(4, Pin.IN, Pin.PULL_UP)
