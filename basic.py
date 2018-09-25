

from __future__ import print_function
from dronekit import connect, VehicleMode, APIException
import socket
import exceptions
from sys import exit

# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(
    description='DroneKit experiments.')
parser.add_argument('--connect',
                    help="vehicle connection target string. If not specified, script connects to 127.0.0.1:14550 by default.")
args = parser.parse_args()

connection_string = args.connect

if not connection_string:
    connection_string = "127.0.0.1:14550"

# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))

try:
    vehicle = connect(connection_string, heartbeat_timeout=15, wait_ready=True)

# Bad TCP connection
except socket.error:
    print ('No server exists!')
    exit(1)

# Bad TTY connection
except exceptions.OSError as e:
    print ('No serial exists!')
    exit(1)

# API Error
except APIException:
    print ('Timeout!')
    exit(1)

# Other error
except:
    print ('Some other error!')
    exit(1)

# Don't try to arm until autopilot is ready
while not vehicle.is_armable:
    print(" Waiting for vehicle to initialise...")
    time.sleep(1)

# Get some vehicle attributes (state)
print("Get some vehicle attribute values:")
print(" GPS: %s" % vehicle.gps_0)
print(" Battery: %s" % vehicle.battery)
print(" Last Heartbeat: %s" % vehicle.last_heartbeat)
print(" Is Armable?: %s" % vehicle.is_armable)
print(" System status: %s" % vehicle.system_status.state)
print(" Mode: %s" % vehicle.mode.name)    # settable

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
print("Completed")
