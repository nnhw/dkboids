from __future__ import print_function
from dronekit import VehicleMode
import argparse
import cmd
import time
from threading import Thread

import connection
import guidance


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
    id = 255
else:
    id = int(args.id)

boids_number = 10


def start_data_flow_out():
    data_flow_out_thread = Thread(target=data_flow_handler_out)
    data_flow_out_thread.daemon = True
    data_flow_out_thread.start()


def start_data_flow_in():
    data_flow_in_thread = Thread(target=data_flow_handler_in)
    data_flow_in_thread.daemon = True
    data_flow_in_thread.start()


def data_flow_handler_out():
    global base_update_rate_hz
    counter = 0
    while True:
        time.sleep(1/base_update_rate_hz)
        connection_buddy.send_data((vehicle._id, counter, vehicle._flight_level, vehicle.location.global_relative_frame.lat,
                                    vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.alt, vehicle.groundspeed))
        counter += 1


def data_flow_handler_in():
    global base_update_rate_hz
    global swarming
    while True:
        time.sleep(1/(base_update_rate_hz*boids_number))
        data = connection_buddy.receive_data()
        vehicle.analyze_data(data)
        if swarming is True:
            vehicle.implement_corrections()
            vehicle.goto_poi()


class ConvertShell(cmd.Cmd):
    intro = 'Welcome to the Converter shell. Type help or ? to list commands.\n'
    prompt = '(command) '

    def do_takeoff(self, arg):
        'takeoff <altitude>; load a program, takeoff and reach target altitude'
        flight_level = int((parse(arg))[0])
        vehicle._flight_level = flight_level
        guidance.takeoff(vehicle, flight_level, args.safety)
        print("Taking off completed")

    def do_print_buddy(self, arg):
        'get buddy info'
        print(vehicle.get_buddy(int(parse(arg)[0])))

    def do_follow(self, arg):
        'follow target'
        vehicle.mode = VehicleMode("GUIDED")
        vehicle._follow_target_id = int(parse(arg)[0])

    def do_stop_follow(self, arg):
        'stop following'
        vehicle._follow_target_id = 0

    def do_swarm(self, arg):
        'enable swarming behavior'
        global swarming
        swarming = True

    def do_stop_swarm(self, arg):
        'disable swarming behavior'
        global swarming
        swarming = False

    def do_set_global_poi(self, arg):
        'set global point of interest'
        connection_buddy.send_data((200, 0, 0, float((parse(arg))[0]), float(
            (parse(arg))[1]), float((parse(arg))[2]), 0))

    def do_bye(self, arg):
        'Exit'
        vehicle.close()
        print('Good Bye')
        return True


def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    if not arg:
        return 0
    else:
        return tuple(arg.split())


if __name__ == "__main__":
    base_update_rate_hz = 1
    swarming = False
    vehicle = connection.safe_dk_connect(args.master, args.baud, id)
    connection_buddy = connection.buddy_connection(8000)
    start_data_flow_out()
    start_data_flow_in()
    ConvertShell().cmdloop()
