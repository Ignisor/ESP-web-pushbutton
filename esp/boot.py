import esp; esp.osdebug(None)

import socket
import sys
import time

import machine
import network

TIMEOUT = 5
URL = 'http://door.gowombat.team/open/'
LED = machine.Pin(1, machine.Pin.OUT)


LED.value(0)  # enable LED

ap_if = network.WLAN(network.AP_IF)
sta_if = network.WLAN(network.STA_IF)

ap_if.active(False)
sta_if.active(True)

# connect to wifi
t_start = time.time()
sta_if.connect("wombat_3", "fantomas")

while not sta_if.isconnected():
    t = time.time() - t_start
    if t >= TIMEOUT:
        break

# send post request to open door
if sta_if.isconnected():
    _, _, host, path = URL.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]

    s = socket.socket()
    try:
        s.connect(addr)
        s.send(bytes('POST /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    except OSError as e:
        # write exception to file
        with open('error.log', 'w') as err_file:
            sys.print_exception(e, err_file)

    s.close()

LED.value(1)  # disable LED
machine.deepsleep()
