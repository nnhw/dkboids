from __future__ import print_function
from dronekit import VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import argparse
import connection
import guidance
import cmd

parser = argparse.ArgumentParser(
    description='DroneKit experiments.')
parser.add_argument('--connect',
                    help="vehicle connection target string. If not specified, script connects to 127.0.0.1:14551 by default.")
parser.add_argument('--baud',
                    help="baudrate of the serial connections. Default is 115200.")
parser.add_argument('--safety',
                    help="on/off - disable or enable safety checks. Default is on")

args = parser.parse_args()


vehicle = connection.safe_connect(args.connect, args.baud)


class ConvertShell(cmd.Cmd):
    intro = 'Welcome to the Converter shell. Type help or ? to list commands.\n'
    prompt = '(command) '

    def do_takeoff(self, arg):
        'takeoff <altitude>; load a program, takeoff and reach target altitude'
        guidance.takeoff(vehicle, parse(arg), args.safety)
        print("Completed")

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
    ConvertShell().cmdloop()
