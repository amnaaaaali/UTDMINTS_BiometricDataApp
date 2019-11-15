'''
    Example for how to send and receive discovery info from glasses on network.

    Team Tobii Notes:
        - tested with Python 3.7 on Windows 10 and MSYS2 (64 bit ver)
        - connects only wifi 10/4/19

'''
import socket
import struct
import json

MULTICAST_ADDR = 'ff02::1'  # all ipv6 devices with link-local scope
PORT = 13007  # Port used by RU


def discover():
    """ Sends discovery info to glass on WLAN.
        Returns the IPv4 of the glasses that recived the discovery-message.
    """
    # Create udp socket
    s6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    # avoid error 'Adress already in use'
    s6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # associate the socket with a specific network interface & port number
    s6.bind(('::', PORT))
    # send data/msg to socket
    s6.sendto('{"type":"discover"}'.encode(), (MULTICAST_ADDR, 13006))

    print("Press Ctrl-C to abort...")
    while True:
        data, address = s6.recvfrom(1024)
        #TypeError: can only concatenate str (not "bytes") to str
        #print(" From: " + address[0] + " " + data)
        # covert data to str
        print(" From: " + address[0] + " " + data.decode())
        #data is returned as json
        data = json.loads(data)
        # get ip address from data
        glasses_IP = data['ipv4']
        # address found
        if len(glasses_IP) > 0:
            print("Discovery Successful.")
            break
    return glasses_IP


if __name__ == '__main__':
    discover()
