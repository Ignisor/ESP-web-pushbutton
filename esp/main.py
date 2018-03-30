import machine
import network
import socket
import sys
import time

LED = machine.Pin(1, machine.Pin.OUT)
BUTTON =  machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
sta_if = network.WLAN(network.STA_IF)
URL = 'http://door.gowombat.team/open/'


def send_open_request():
    LED.value(0)

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

    LED.value(1)


while True:
    if BUTTON.value() == 0:
        send_open_request()

    time.sleep(0.1)
