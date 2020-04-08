#!/usr/bin/env python

from __future__ import print_function

from random import randint

import can
from can.bus import BusState

def service1(bus, msg):
    if msg.data[2] == 0x00:
        print(">> Caps")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x06, 0x41, 0x00, 0xBF, 0xDF, 0xB9, 0x91],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x0B:
        print(">> Intake manifold absolute pressure")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x04, 0x41, 0x0B, randint(10, 40)],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x0C:
        print(">> RPM")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x04, 0x41, 0x0C, randint(18, 70), randint(0, 255)],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x0D:
        print(">> Speed")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x03, 0x41, 0x0D, randint(40, 60)],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x0F:
        print(">> Intake air temperature")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x03, 0x41, 0x0F, randint(60, 64)],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x10:
        print(">> MAF air flow rate")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x04, 0x41, 0x10, 0x00, 0xFA],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x04:
        print(">> Calculated engine load")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x03, 0x41, 0x04, 0x20],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x05:
        print(">> Engine coolant temperature")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x03, 0x41, 0x05, randint(88 + 40, 95 + 40)],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x11:
        print(">> Throttle position")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x03, 0x41, 0x11, randint(20, 60)],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x33:
        print(">> Absolute Barometric Pressure")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x03, 0x41, 0x33, randint(20, 60)],
          is_extended_id=False)
        bus.send(msg)
    else:
        print("!!! Service 1, unknown code", msg.data[2])


def receive_all():

    bus = can.interface.Bus(bustype='socketcan',channel='can0')
    #bus = can.interface.Bus(bustype='ixxat', channel=0, bitrate=250000)
    #bus = can.interface.Bus(bustype='vector', app_name='CANalyzer', channel=0, bitrate=250000)

    #bus.state = BusState.ACTIVE
    #bus.state = BusState.PASSIVE

    try:
        while True:
            msg = bus.recv(1)
            if msg is not None:
                #print(msg)
                if msg.arbitration_id == 0x7df and msg.data[1] == 0x01:
                    service1(bus, msg)
                else:
                    print("Unknown ID", msg.arbitration_id, "or service code", msg.data[1])

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    receive_all()
