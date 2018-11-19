import time
import network
import machine

from data import configure

ap_if = network.WLAN(network.AP_IF)
sta_if = network.WLAN(network.STA_IF)


def toggle_wifi(status=True):
    """Enables or disables wi-fi for connection"""
    sta_if.active(status)


def toggle_hotspot(status=True):
    """Enables or disables hotspot (ap_if)"""
    ap_if.active(status)


def connect(ssid=None, password=None, indicate=True):
    """Tries to connect to the wi-fi network"""
    if indicate:  # this is required because LED pin is blocking serial interface on ESP-01
        from utils.pins import LED

    ssid = ssid or configure.SSID
    password = password or configure.PASSWORD

    for i in range(configure.CONNECT_RETRIES):
        t_start = time.time()
        sta_if.connect(ssid, password)

        while not sta_if.isconnected():
            if indicate:
                LED.value(0)  # 0 - is enable for LED
                time.sleep(0.1)
                LED.value(1)
            time.sleep(0.1)

            t = time.time() - t_start
            if t >= configure.CONNECTION_TIME:
                break

        if sta_if.isconnected():
            return sta_if.isconnected()


def reset_if_not_connected():
    if sta_if.isconnected():
        return True
    else:
        machine.reset()
        return False