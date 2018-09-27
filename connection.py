from __future__ import print_function
from dronekit import connect, APIException

import socket
import exceptions
from sys import exit

def safe_connect(connection_string,baudrate):
    

    if not connection_string:
        connection_string = "127.0.0.1:14551"

    if not baudrate:
        baudrate = 57600

    # Connect to the Vehicle.
    print("Connecting to vehicle on: %s" % (connection_string,))

    try:
        vehicle = connect(connection_string, baud=baudrate,
                          heartbeat_timeout=15, wait_ready=True)

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
