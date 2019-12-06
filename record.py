""" 
    Modified calibrate_and_record.py example provided by Tobii.
    Module handles recording.

    Recording requires participant id created during calibration.

    Tested with Python 3.7 on Windows 10 and MSYS2 64-bit
    Uses gsocket and not python sockets.
    For ethernet connection only.
"""

import urllib.request  #updated version
import json
import time
import threading
import gi
from gi.repository import Gio, GLib

# Keep-alive message content used to request live video streams
KA_VIDEO_MSG = {"type": "live.video.unicast", "key": "some_UID", "op": "start"}
PORT = ':80'  # Port number required to access REST API using IPV6 address for ethernet connection


# Create UDP gsocket
def mkgsock(peer):
    """ Create a upd Gsocket pair for a peer description """
    ipfam = Gio.SocketFamily.IPV4
    if ':' in peer[0]:
        ipfam = Gio.SocketFamily.IPV6
    return Gio.Socket.new(ipfam, Gio.SocketType.DATAGRAM,
                          Gio.SocketProtocol.UDP)


class KeepAlive:
    """ Sends keep-alive signals to a peer via a gsocket """
    _sig = 0

    def __init__(self, gsock, peer, keep_alive_msg, timeout=1):
        # Convert keep alive message to JSON
        jsonobj = json.dumps(keep_alive_msg)
        gaddr = Gio.InetSocketAddress.new_from_string(str(peer[0]),
                                                      int(peer[1]))
        # Send keep alive message to glasses. JSON is converted to bytes
        gsock.send_to(gaddr, jsonobj.encode(), None)
        # Set timeout function to be called every second
        self._sig = GLib.timeout_add_seconds(timeout, self._timeout, gsock,
                                             peer, jsonobj)

    # Resends keep alive message
    def _timeout(self, gsock, peer, jsonobj):
        gaddr = Gio.InetSocketAddress.new_from_string(str(peer[0]),
                                                      int(peer[1]))
        gsock.send_to(gaddr, jsonobj.encode(), None)
        return True

    def stop(self):
        GLib.source_remove(self._sig)


def post_request(base_url, api_action, data=None):
    """ Sends data to URL """
    url = base_url + api_action
    req = urllib.request.Request(url)
    # Header is key:value pair
    req.add_header('Content-Type', 'application/json')
    data = json.dumps(data)
    response = urllib.request.urlopen(req, data.encode())
    data = response.read()
    json_data = json.loads(data)
    return json_data


def wait_for_status(base_url, api_action, key, values):
    url = base_url + api_action
    running = True
    while running:
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib.request.urlopen(req, None)
        data = response.read()
        json_data = json.loads(data)
        if json_data[key] in values:
            running = False
        time.sleep(1)
    return json_data[key]


def create_recording(base_url, participant_id):
    """ Creates recording and returns recordin id """
    data = {'rec_participant': participant_id}
    json_data = post_request(base_url, '/api/recordings', data)
    return json_data['rec_id']


def start_recording(glasses_ip, participant_id):
    """ Starts recording using REST API. Return recording ID needed to stop recording """
    base_url = 'http://' + str(glasses_ip) + PORT
    recording_id = create_recording(base_url, participant_id)
    print('Recording started...')
    post_request(base_url, '/api/recordings/' + recording_id + '/start')
    return (recording_id)


def stop_recording(glasses_ip, recording_id):
    """ Stops the recording with the given recording id.
        Returns the stauts of the recording. """
    print('Stopping recording...')
    base_url = 'http://' + str(glasses_ip) + PORT
    post_request(base_url, '/api/recordings/' + recording_id + '/stop')
    status = wait_for_status(base_url,
                             '/api/recordings/' + recording_id + '/status',
                             'rec_state', ['failed', 'done'])
    return status