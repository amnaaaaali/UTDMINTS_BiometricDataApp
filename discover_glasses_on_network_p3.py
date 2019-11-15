'''
    Example for how to send and receive discovery info from glasses on network.

    Note: This example program is tested with Python 2.7 on Ubuntu 12.04 LTS (precise),
          Ubuntu 14.04 LTS (trusty), and Windows 8. 

    Team Tobii Notes:
        - runs on Windows 10 9/9/19 via python27
        - error: TypeError: can only concatenate str (not "bytes") to str
            >> decoded 'data' = resolved 9/16/19
        - doesn't connect via ethernet, only wifi 10/4/19

'''
import socket
import struct

MULTICAST_ADDR = 'ff02::1'  # all ipv6 devices with link-local scope
PORT = 13007  # Port used by RU

if __name__ == '__main__':

    # Create udp socket
    s6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    # avoid error 'Adress already in use'
    s6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # associate the socket with a specific network interface & port number
    # :: is equivalent to 0.0.0.0
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
