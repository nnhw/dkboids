from __future__ import print_function
from dronekit import VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import argparse
import connection
import guidance
import cmd
import time
from threading import Thread
import sys
import struct

parser = argparse.ArgumentParser(
    description='DroneKit experiments.')
parser.add_argument('--master',
                    help="vehicle connection target string. If not specified, script connects to 127.0.0.1:14551 by default.")
parser.add_argument('--baud',
                    help="baudrate of the serial connections. Default is 115200.")
parser.add_argument('--safety',
                    help="on/off - disable or enable safety checks. Default is on")
parser.add_argument('--id',
                    help="mavlink system ID of this instance")

args = parser.parse_args()

if not args.id:
    id=255
else:
    id = int(args.id)

def start_data_flow_out():
    data_flow_out_thread = Thread(target=data_flow_handler_out)
    data_flow_out_thread.daemon = True
    data_flow_out_thread.start()

def start_data_flow_in():
    data_flow_in_thread = Thread(target=data_flow_handler_in)
    data_flow_in_thread.daemon = True
    data_flow_in_thread.start()

def data_flow_handler_out():
    global update_rate_hz
    while True:
        time.sleep(1/update_rate_hz)
        data = struct.pack('!ifff', id, vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.alt)
        connection_buddy.send_data(data)

def data_flow_handler_in():
    global update_rate_hz
    while True:
        time.sleep(1/update_rate_hz)
        data = connection_buddy.receive_data(1024)
        print(struct.unpack('!ifff', data))

class ConvertShell(cmd.Cmd):
    intro = 'Welcome to the Converter shell. Type help or ? to list commands.\n'
    prompt = '(command) '

    def do_takeoff(self, arg):
        'takeoff <altitude>; load a program, takeoff and reach target altitude'
        guidance.takeoff(vehicle, parse(arg), args.safety)
        print("Taking off completed")

    def do_send(self, arg):
        connection_buddy.send_data("kek!")

    def do_receive(self, arg):
        data = connection_buddy.receive_data(1024)
        print(data)

    def do_start_flow_out(self, arg):
        'Start outgoing data flow'
        start_data_flow_out()

    def do_start_flow_in(self, arg):
        'Start incoming data flow'
        start_data_flow_in()

    def do_bye(self, arg):
        'Exit'
        vehicle.close()
        print('Good Bye')
        return True


def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    # return tuple(map(int, arg.split()))
    if not arg:
        return 0
    else:
        return int(arg)


if __name__ == "__main__":
    vehicle = connection.safe_dk_connect(args.master, args.baud, id)
    connection_buddy = connection.socket_connection(8000)
    update_rate_hz = 1
    ConvertShell().cmdloop()
