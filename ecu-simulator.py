#!/usr/bin/env python

from __future__ import print_function

from random import randint

import logging as log
import getopt, sys

import can
from can.bus import BusState

def service1(bus, msg):
    if msg.data[2] == 0x00:
        log.debug(">> Caps")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x06, 0x41, 0x00, 0xBF, 0xDF, 0xB9, 0x91],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x04:
        log.debug(">> Calculated engine load")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x03, 0x41, 0x04, 0x20],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x05:
        log.debug(">> Engine coolant temperature")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x03, 0x41, 0x05, randint(88 + 40, 95 + 40)],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x0B:
        log.debug(">> Intake manifold absolute pressure")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x04, 0x41, 0x0B, randint(10, 40)],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x0C:
        log.debug(">> RPM")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x04, 0x41, 0x0C, randint(18, 70), randint(0, 255)],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x0D:
        log.debug(">> Speed")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x03, 0x41, 0x0D, randint(40, 60)],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x0F:
        log.debug(">> Intake air temperature")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x03, 0x41, 0x0F, randint(60, 64)],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x10:
        log.debug(">> MAF air flow rate")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x04, 0x41, 0x10, 0x00, 0xFA],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x11:
        log.debug(">> Throttle position")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x03, 0x41, 0x11, randint(20, 60)],
          is_extended_id=False)
        bus.send(msg)
    elif msg.data[2] == 0x33:
        log.debug(">> Absolute Barometric Pressure")
        msg = can.Message(arbitration_id=0x7e8,
          data=[0x03, 0x41, 0x33, randint(20, 60)],
          is_extended_id=False)
        bus.send(msg)
    else:
        log.warning("!!! Service 1, unknown code 0x%02x", msg.data[2])


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
                    log.warning("Unknown ID %d or service code 0x%02x", msg.arbitration_id, msg.data[1])

    except KeyboardInterrupt:
        pass

def usage():
    # DOTO: implement
    pass

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:v", ["loglevel="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    loglevel = "INFO"

    for o, a in opts:
        if o == "-v":
            loglevel = "DEBUG"
        elif o in ("-l", "--loglevel"):
            loglevel = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

    numeric_level = getattr(log, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    log.basicConfig(level=numeric_level)
    receive_all()

if __name__ == "__main__":
    main();
