'''
    Example for how to receive live data and display live video (without gaze overlay) from glasses.
    gstreamer 0.10 required in order to display live video.

    Note: This example program is *only* tested with Python 2.7 on Ubuntu 12.04 LTS
          and Ubuntu 14.04 LTS (running natively).

    Team Tobii Notes:
        - tested with Python 3.7 on Windows 10 and MSYS2 (64bit ver)
        - connects to glasses on Wifi only
        - see livestream_p3_readme.txt for additional notes
    
'''
import time
import socket
import threading
import signal
import sys

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, Gio

timeout = 1.0
running = True

GLASSES_IP = "192.168.71.50"  # IPv4 address on wlan
PORT = 49152  #for UDP

# Keep-alive message content used to request live data and live video streams
KA_DATA_MSG = "{\"type\": \"live.data.unicast\", \"key\": \"some_GUID\", \"op\": \"start\"}"
KA_VIDEO_MSG = "{\"type\": \"live.video.unicast\", \"key\": \"some_other_GUID\", \"op\": \"start\"}"

# Gstreamer pipeline definition used to decode and display the live video stream

PIPELINE_DEF = "udpsrc name=src do-timestamp=true name=src blocksize=1316 closefd=false buffer-size=5600!" \
                "tsparse !" \
                "tsdemux !" \
                "queue !" \
                "h264parse !" \
                "avdec_h264 max-threads=0 !" \
                "d3dvideosink force-aspect-ratio=True"


# Create UDP socket
def mksock(peer):
    iptype = socket.AF_INET
    if ':' in peer[0]:
        iptype = socket.AF_INET6
    return socket.socket(iptype, socket.SOCK_DGRAM)


# Callback function
def send_keepalive_msg(socket, msg, peer):
    while running:
        print("Sending " + msg + " to target " + peer[0] + " socket no: " +
              str(socket.fileno()) + "\n")
        # need to encode msg since byte-like obj is required
        socket.sendto(msg.encode(), peer)
        time.sleep(timeout)


def signal_handler(signal, frame):
    stop_sending_msg()
    sys.exit(0)


def stop_sending_msg():
    global running
    running = False


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    peer = (GLASSES_IP, PORT)

    # Create socket which will send a keep alive message for the live data stream
    data_socket = mksock(peer)
    td = threading.Timer(0, send_keepalive_msg,
                         [data_socket, KA_DATA_MSG, peer])
    td.start()

    # Create socket which will send a keep alive message for the live video stream
    video_socket = mksock(peer)
    tv = threading.Timer(0, send_keepalive_msg,
                         [video_socket, KA_VIDEO_MSG, peer])
    tv.start()

    # Create gstreamer pipeline and connect live video socket to it
    Gst.init(None)
    pipeline = Gst.Pipeline.new()

    try:
        pipeline = Gst.parse_launch(PIPELINE_DEF)

    except Exception as e:
        print(e)
        stop_sending_msg()
        sys.exit(0)

    # Get element by name
    src = pipeline.get_by_name("src")

    # create gsocket obj to pass the pipeline's udpsrc element property called socket
    gsock = Gio.Socket.new_from_fd(video_socket.fileno())
    src.set_property("socket", gsock)

    pipeline.set_state(Gst.State.PLAYING)

    while running:
        # Read live data
        data, address = data_socket.recvfrom(1024)
        print(data.decode())

        state_change_return, state, pending_state = pipeline.get_state(0)

        if Gst.StateChangeReturn.FAILURE == state_change_return:
            stop_sending_msg()
