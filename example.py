#!/usr/bin/python3
import time
import sys
import logging
from pyhomematic import HMConnection

logging.basicConfig(level=logging.DEBUG)

DEVICE1 = 'address_of_rollershutter_device'  # e.g. KEQ7654321
DEVICE2 = 'address_of_doorcontact'  # e.g. LEQ1234567
DEVICE3 = 'address_of_thermostat'


def systemcallback(src, *args):
    pass
    # print(src)
    # for arg in args:
    #     print(arg)


try:
    # Create a server that listens on 127.0.0.1:7080 and identifies itself as myserver.
    # Connect to Homegear at 127.0.0.1:2001
    # Automatically start everything. Without autostart, pyhomematic.start() can be called.
    # We add a systemcallback so we can see what else happens besides the regular events.
    pyhomematic = HMConnection(interface_id="homematic",
                               autostart=True,
                               systemcallback=systemcallback,
                               remotes={
                                   "Funk": {
                                       "ip": "10.0.1.29",
                                       "port": 2001,
                                       "username": "Olli",
                                       "password": "Oll!Sued20"},

                                   "HMIP": {
                                       "ip": "10.0.1.29",
                                       "port": 2010,
                                       "username": "Olli",
                                       "password": "Oll!Sued20"},

                               })
except Exception:
    sys.exit(1)

sleepcounter = 0


def eventcallback(address, interface_id, key, value):
    print("CALLBACK: %s, %s, %s, %s" % (address, interface_id, key, value))


while not pyhomematic.devices and sleepcounter < 20:
    print("Waiting for devices")
    sleepcounter += 1
    time.sleep(1)
# print(pyhomematic.devices)


for interface, deviceDict in pyhomematic.devices.items():
    for key, device in deviceDict.items():
        device.getDeviceDescription()
        print(device.FULLNAME)


# Get level of rollershutter from 0.0 to 1.0.
print(pyhomematic.devices[DEVICE1].get_level())

# Set level of rollershutter to 50%.
pyhomematic.devices[DEVICE1].set_level(0.5)
time.sleep(10)

# Move rollershutter down.
pyhomematic.devices[DEVICE1].move_down()
time.sleep(10)

# Get level of rollershutter from 0.0 to 1.0 directly from channel.
print(pyhomematic.devices_all[DEVICE1 + ':1'].getValue("LEVEL"))

# Check if doorcontact is open by querying the device.
print(pyhomematic.devices[DEVICE2].is_open())

# Check if doorcontact is open or closed by querying the device-channel. True or False, depending on state.
print(pyhomematic.devices_all[DEVICE2 + ':1'].getValue("STATE"))

# Get Actual Temperature
print(pyhomematic.devices[DEVICE3].actual_temperature)

# Get Set Temperature
print(pyhomematic.devices[DEVICE3].set_temperature)

# Get Battery State
print(pyhomematic.devices[DEVICE3].battery_state)

# Set an eventcallback for the doorcontact that should be called when events occur.
pyhomematic.devices[DEVICE2].setEventCallback(eventcallback)
time.sleep(10)
# Now open / close doorcontact and watch the eventcallback being called.

# Stop the server thread so Python can exit properly.
pyhomematic.stop()

sys.exit(0)
