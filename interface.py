from __future__ import print_function
from dronekit import VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import argparse
import connection
import guidance
import cmd
import time
from threading import Thread
import sys

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

def start_data_flow():
    data_flow_thread = Thread(target=data_flow_handler)
    data_flow_thread.daemon = True
    data_flow_thread.start()

def data_flow_handler():
    global update_rate_hz
    while True:
        time.sleep(1/update_rate_hz)
        data = connection_buddy.receive_data(1024)
        print(data)


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

    def do_start_flow(self, arg):
        'Start data flow'
        start_data_flow()

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
    # vehicle = connection.safe_dk_connect(args.master, args.baud, args.id)
    connection_buddy = connection.socket_connection(8000)
    update_rate_hz = 10
    ConvertShell().cmdloop()