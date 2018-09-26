

from __future__ import print_function
from dronekit import connect, VehicleMode, APIException, LocationGlobalRelative, LocationGlobal, Command
from pymavlink import mavutil
import socket
import exceptions
from sys import exit
import argparse
import time

parser = argparse.ArgumentParser(
    description='DroneKit experiments.')
parser.add_argument('--connect',
                    help="vehicle connection target string. If not specified, script connects to 127.0.0.1:14550 by default.")
args = parser.parse_args()

def safe_connect():
    connection_string = args.connect

    if not connection_string:
        connection_string = "127.0.0.1:14551"

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

    return vehicle

def arm_and_takeoff(aVehicle,aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    download_mission()

    cmds = vehicle.commands

    print(" Clear any existing commands")
    cmds.clear() 

    #Add MAV_CMD_NAV_TAKEOFF command. This is ignored if the vehicle is already in the air.
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 50))
    print(" Upload new commands to vehicle")
    cmds.upload()

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not aVehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Plane should arm first
    aVehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not aVehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    # Setting mode to AUTO
    aVehicle.mode = VehicleMode("AUTO")
    print("Taking off!")
    # aVehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", aVehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if aVehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

def download_mission():
    """
    Download the current mission from the vehicle.
    """
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready() # wait until download is complete.

vehicle = safe_connect()

if vehicle.groundspeed < 0.1:
    print("Arming and taking-off!")
    arm_and_takeoff(vehicle,50);
    print("Set default/target airspeed to 30")
    vehicle.groundspeed = 30
else:
    print("Looks like the vehicle is in flight already!")

vehicle.mode = VehicleMode("GUIDED")


# print("Returning to Launch")
# vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
vehicle.close()

print("Completed")
