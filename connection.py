from __future__ import print_function
from dronekit import connect, APIException

import socket
import exceptions
import socket
from sys import exit

def safe_dk_connect(connection_string,baudrate):

    if not connection_string:
        connection_string = "127.0.0.1:14551"

    if not baudrate:
        baudrate = 57600
    else:
        baudrate = int(baudrate)

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

class socket_connection:
    def __init__(self, l_port=00):
        self._port = l_port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(('', self._port))
        self._data_rcv = b''
        self._data_send = b''        

    def send_data(self, l_data):
        self._data_send = l_data
        self._sock.sendto(self._data_send, ("", self._port))

    def receive_data(self, l_size):
        self._data_rcv = self._sock.recvfrom(l_size)[0]
        return self._data_rcv
           
