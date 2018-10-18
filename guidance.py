from __future__ import print_function
from dronekit import connect, VehicleMode, APIException, LocationGlobalRelative, LocationGlobal, Command
from pymavlink import mavutil

import time
import math
import connection


def takeoff(vehicle, target_altitude, safety):
    if not safety:
        safety = True
    else:
        if safety == "on":
            safety = True
        elif safety == "off":
            safety = False

    if 0 == target_altitude:
        print('Setting default altitude 50m')
        target_altitude = 50

    my_location_alt = vehicle.location.global_frame
    my_location_alt.alt = my_location_alt.alt + target_altitude
    vehicle.home_location = my_location_alt

    print("New home location altitude is set to ", vehicle.home_location.alt)

    print(" Write vehicle param 'ALT_HOLD_RTL' : ", target_altitude*100)
    vehicle.parameters['ALT_HOLD_RTL'] = target_altitude*100

    if safety is True:
        if vehicle.groundspeed < 0.3:
            print("Arming and taking-off!")
            arm_and_takeoff(vehicle, target_altitude, safety)
            print("Set default/target airspeed to 30")
            vehicle.airspeed = 30
        else:
            print("Looks like the vehicle is in flight already!")
    else:
        print("Ignoring everything, trying to take off")
        arm_and_takeoff(vehicle, target_altitude, safety)


def arm_and_takeoff(vehicle, aTargetAltitude, safety):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    download_mission(vehicle)

    cmds = vehicle.commands

    print(" Clear any existing commands")
    cmds.clear()

    # Add MAV_CMD_NAV_TAKEOFF command. This is ignored if the vehicle is already in the air.
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, aTargetAltitude))
    print(" Upload new commands to vehicle")
    cmds.upload()
    time.sleep(3)

    if safety is True:
        print("Basic pre-arm checks")
        # Don't try to arm until autopilot is ready
        while not vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

    print("Arming motors")
    # Plane should arm first
    vehicle.armed = True
    time.sleep(3)

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Trying to arm again...")
        vehicle.armed = True
        time.sleep(1)

    # Setting mode to AUTO
    vehicle.mode = VehicleMode("AUTO")
    print("Taking off!")
    time.sleep(3)

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


def download_mission(vehicle):
    """
    Download the current mission from the vehicle.
    """
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()  # wait until download is complete.


def set_attitude(vehicle, roll_angle=0.0, pitch_angle=0.0, yaw_rate=0.0, thrust=0.5, duration=0):
    # Thrust >  0.5: Ascend
    # Thrust == 0.5: Hold the altitude
    # Thrust <  0.5: Descend
    msg = vehicle.message_factory.set_attitude_target_encode(
        0,  # time_boot_ms
        1,  # Target system
        1,  # Target component
        0b00000000,  # Type mask: bit 1 is LSB
        to_quaternion(roll_angle, pitch_angle),  # Quaternion
        0,  # Body roll rate in radian
        0,  # Body pitch rate in radian
        math.radians(yaw_rate),  # Body yaw rate in radian
        thrust  # Thrust
    )
    vehicle.send_mavlink(msg)

    start = time.time()
    while time.time() - start < duration:
        vehicle.send_mavlink(msg)
        time.sleep(0.1)


def to_quaternion(roll=0.0, pitch=0.0, yaw=0.0):
    """
    Convert degrees to quaternions
    """
    t0 = math.cos(math.radians(yaw * 0.5))
    t1 = math.sin(math.radians(yaw * 0.5))
    t2 = math.cos(math.radians(roll * 0.5))
    t3 = math.sin(math.radians(roll * 0.5))
    t4 = math.cos(math.radians(pitch * 0.5))
    t5 = math.sin(math.radians(pitch * 0.5))

    w = t0 * t2 * t4 + t1 * t3 * t5
    x = t0 * t3 * t4 - t1 * t2 * t5
    y = t0 * t2 * t5 + t1 * t3 * t4
    z = t1 * t2 * t4 - t0 * t3 * t5

    return [w, x, y, z]
