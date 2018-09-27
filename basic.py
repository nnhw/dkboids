from __future__ import print_function
from dronekit import VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import argparse
import connection
import guidance

parser = argparse.ArgumentParser(
    description='DroneKit experiments.')
parser.add_argument('--connect',
                    help="vehicle connection target string. If not specified, script connects to 127.0.0.1:14551 by default.")
args = parser.parse_args()

connection_string = args.connect
vehicle = connection.safe_connect(connection_string)
guidance.safe_takeoff(vehicle,50)

# Close vehicle object before exiting script
vehicle.close()

print("Completed")
