import machine
import ubinascii

from umqtt.simple import MQTTClient
from data import configure
from utils.pins import BUTTON, OFF, ON


CLIENT_ID = ubinascii.hexlify(machine.unique_id())
mqtt = MQTTClient(CLIENT_ID, configure.MQTT_SERVER)
mqtt.connect()


def check_button(pressed):
    mqtt.publish('button/pressed/{}'.format(CLIENT_ID).encode(), str('down' if pressed else 'up').encode())


pressed_button = False
while True:
    try:
        if pressed_button == False and BUTTON.value() == ON:
            check_button(True)
            pressed_button = True
        elif pressed_button == True and BUTTON.value() == OFF:
            check_button(False)
            pressed_button = False
    except Exception as e:
        with open('errors.txt', 'a') as err_file:
            err_file.write(str(e))
            err_file.write('\n')
        mqtt.publish('errors/{}'.format(CLIENT_ID).encode(), str(e).encode())

mqtt.disconnect()

machine.reset()
