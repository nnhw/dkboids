from __future__ import print_function
from dronekit import VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import argparse
import connection
import guidance

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
guidance.takeoff(vehicle,50, args.safety)

# Close vehicle object before exiting script
vehicle.close()

print("Completed")
