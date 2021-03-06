import esp; esp.osdebug(None)

import socket
import sys
import time

import machine
import network

TIMEOUT = 5
URL = 'http://door.gowombat.team/open/'
LED = machine.Pin(1, machine.Pin.OUT)


# enable LED
LED.value(0)

sta_if = network.WLAN(network.STA_IF)
if not sta_if.active():
    sta_if.active(True)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

# connect to wifi (most settings specified as statics for speedup)
sta_if.ifconfig(('192.168.1.82', '255.255.255.0', '192.168.1.1', '192.168.1.1'))
sta_if.config(mac=b'\x18\xfe4\xd5i\x1c', dhcp_hostname='ESP_D5691C')
sta_if.connect("wombat_3", "fantomas", bssid=b'\xd8P\xe6\xd9$\x10')

t_start = time.time()
while not sta_if.isconnected():
    t = time.time() - t_start
    if t >= TIMEOUT:
        break

# send post request to open door
if sta_if.isconnected():
    _, _, host, path = URL.split('/', 3)

    try:
        host, port = host.split(':')
        port = int(port)
    except ValueError as e:
        port = 80

    try:
        # try to get address info from domain name
        addr = socket.getaddrinfo(host, port)[0][-1]
    except OSError:
        # then just parse IP
        addr = (host, port)

    s = socket.socket()
    try:
        s.connect(addr)
        s.send(bytes('POST /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
        time.sleep(1)
    except OSError as e:
        # write exception to file
        with open('error.log', 'w') as err_file:
            sys.print_exception(e, err_file)

    s.close()

LED.value(1)  # disable LED
machine.deepsleep()
