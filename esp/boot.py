import esp; esp.osdebug(None)

import time

import machine
import network

TIMEOUT = 5
LED = machine.Pin(1, machine.Pin.OUT)


# enable LED
LED.value(0)

sta_if = network.WLAN(network.STA_IF)
if not sta_if.active():
    sta_if.active(True)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

# connect to wifi (most settings specified as statics for speedup)
sta_if.ifconfig(('192.168.1.134', '255.255.255.0', '192.168.1.1', '192.168.1.1'))
sta_if.config(mac=b'\xbc\xdd\xc2\x81\x0c\xba', dhcp_hostname='ESP_810CBA')
sta_if.connect("wombat_3", "fantomas", bssid=b'\xd8\x50\xe6\xd9\x24\x10')

t_start = time.time()
while not sta_if.isconnected():
    t = time.time() - t_start
    if t >= TIMEOUT:
        break

LED.value(1)  # disable LED
