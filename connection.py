from __future__ import print_function
import dronekit
import time

import struct
import socket
import exceptions
import boid_cl
import re
from sys import exit

# threading callback functions


def data_flow_handler_out(vehicle, rate, connection):
    counter = 0
    while True:
        time.sleep(1/rate)
        data = {'id': vehicle._id, 'counter': counter, 'flight_level': vehicle._flight_level, 'lat': vehicle.location.global_relative_frame.lat,
                'lon': vehicle.location.global_relative_frame.lon, 'alt': vehicle.location.global_relative_frame.alt, 'groundspeed': vehicle.groundspeed}
        connection.send_data(data)
        counter += 1


def data_flow_handler_in(vehicle, rate, connection):
    while True:
        time.sleep(1/(rate))
        data = connection.receive_data()
        vehicle.input_data(data)


# inter dkboids connections


class socket_connection(object):
    def __init__(self, l_port=00):
        multicast_addr = '224.3.29.71'
        self._multicast_group = ('224.3.29.71', l_port)
        self._port = l_port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ttl = struct.pack('b', 1)
        self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        group = socket.inet_aton(multicast_addr)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self._sock.setsockopt(
            socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self._sock.bind(('', self._port))

        self._data_rcv = b''
        self._data_send = b''

    def send_data(self, l_data):
        self._data_send = l_data
        self._sock.sendto(self._data_send, self._multicast_group)

    def receive_data(self, l_size):
        self._data_rcv = self._sock.recvfrom(l_size)[0]
        return self._data_rcv


class buddy_connection(socket_connection):
    def __init__(self, port):
        super(buddy_connection, self).__init__(port)

    def _unpack_incoming(self, l_data_rcv):
        data = struct.unpack('!iiiffff', l_data_rcv)
        return {"id": data[0], "counter": data[1], "flight_level": data[2], "lat": data[3], "lon": data[4], "alt": data[5], "groundspeed": data[6]}

    def _pack_outgoing(self, l_data):
        return struct.pack('!iiiffff', l_data['id'], l_data['counter'], l_data['flight_level'],
                           l_data['lat'], l_data['lon'], l_data['alt'], l_data['groundspeed'])

    def send_data(self, l_data):
        socket_connection.send_data(self, self._pack_outgoing(l_data))

    def receive_data(self):
        return self._unpack_incoming(socket_connection.receive_data(self, 1024))


# mavlink
def safe_dk_connect(connection_string, baudrate, id):

    if not connection_string:
        connection_string = "127.0.0.1:14551"

    if not baudrate:
        baudrate = 57600
    else:
        baudrate = int(baudrate)

    # Connect to the Vehicle.
    print("Connecting to vehicle on: %s" % (connection_string,))

    try:
        vehicle = boid_connect(connection_string, baud=baudrate,
                               heartbeat_timeout=15, wait_ready=True, source_system=id)

    # Bad TCP connection
    except socket.error:
        print ('No server exists!')
        exit(1)

    # Bad TTY connection
    except exceptions.OSError as e:
        print ('No serial exists!')
        exit(1)

    # API Error
    except dronekit.APIException:
        print ('Timeout!')
        exit(1)

    # Other error
    except:
        print ('Some other error!')
        exit(1)

    return vehicle


def boid_connect(ip,
                 _initialize=True,
                 wait_ready=None,
                 status_printer=dronekit.errprinter,
                 rate=4,
                 baud=115200,
                 heartbeat_timeout=30,
                 source_system=255,
                 use_native=False):

    handler = dronekit.MAVConnection(
        ip, baud=baud, source_system=source_system, use_native=use_native)
    boid = boid_cl.Boid(handler, source_system)

    if status_printer:

        @boid.on_message('STATUSTEXT')
        def listener(self, name, m):
            status_printer(
                re.sub(r'(^|\n)', '>>> ', m.text.decode('utf-8').rstrip()))

    if _initialize:
        boid.initialize(rate=rate, heartbeat_timeout=heartbeat_timeout)

    if wait_ready:
        if wait_ready == True:
            boid.wait_ready(True)
        else:
            boid.wait_ready(*wait_ready)

    return boid
