""" 
    Modified calibrate_and_record.py example provided by Tobii.
    Creates project, participant, and calibration IDs and attempts to calibrate gaze.
    
    In order to make the calibration pass the keeep-alive message needs to be sent.

    This module is tested with Python 3.7 on Windows 10 and MSYS2 64 bit.
    Uses gsocket and not python sockets.
"""

import urllib.request  #updated version
import json
import time
import threading
import gi
from gi.repository import Gio, GLib

# Keep-alive message content used to request live data
KA_DATA_MSG = {"type": "live.data.unicast", "key": "some_GUID", "op": "start"}


# Creates UDP gsocket
def mkgsock(glasses_ip):
    """ Create a upd Gsocket pair for a peer description """
    ipfam = Gio.SocketFamily.IPV4
    gaddr = Gio.InetAddress.new_from_string(glasses_ip)
    if gaddr.get_family == Gio.SocketFamily.IPV6:
        ipfam = Gio.SocketFamily.IPV6
    return Gio.Socket.new(ipfam, Gio.SocketType.DATAGRAM,
                          Gio.SocketProtocol.UDP)


class KeepAlive:
    """ Sends keep-alive signals to peer via a gsocket """
    _sig = 0

    def __init__(self, gsock, peer, keep_alive_msg, timeout=1):
        jsonobj = json.dumps(keep_alive_msg)
        gaddr = Gio.InetSocketAddress.new_from_string(str(peer[0]),
                                                      int(peer[1]))
        gsock.send_to(gaddr, jsonobj.encode(), None)
        self._sig = GLib.timeout_add_seconds(timeout, self._timeout, gsock,
                                             peer, jsonobj)

    def _timeout(self, gsock, peer, jsonobj):
        gaddr = Gio.InetSocketAddress.new_from_string(str(peer[0]),
                                                      int(peer[1]))
        gsock.send_to(gaddr, jsonobj.encode(), None)
        return True

    def stop(self):
        GLib.source_remove(self._sig)


# Send data to URL
def post_request(base_url, api_action, data=None):
    url = base_url + api_action
    req = urllib.request.Request(url)
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
        #req = urllib2.Request(url)
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        #response = urllib2.urlopen(req, None)
        response = urllib.request.urlopen(req, None)
        data = response.read()
        json_data = json.loads(data)
        if json_data[key] in values:
            running = False
        time.sleep(1)
    return json_data[key]


def create_project(base_url):
    print("Creating project...")
    json_data = post_request(base_url, '/api/projects')
    print("Project created.")
    return json_data['pr_id']


def create_participant(base_url, project_id):
    print("Creating participant...")
    data = {'pa_project': project_id}
    json_data = post_request(base_url, '/api/participants', data)
    print("Participant created.")
    return json_data['pa_id']


def create_calibration(base_url, project_id, participant_id):
    print("Creating calibration...")
    data = {
        'ca_project': project_id,
        'ca_type': 'default',
        'ca_participant': participant_id
    }
    json_data = post_request(base_url, '/api/calibrations', data)
    print("Calibration created.")
    return json_data['ca_id']


def start_calibration(calibration_id, base_url):
    post_request(base_url, '/api/calibrations/' + calibration_id + '/start')


def stop_calibration(gsocket, keepalive):
    """ Stop keep alive message and close gsocket"""
    keepalive.stop()
    gsocket.close()


def calibrate(glasses_ip, port):
    """ Creates project, participant, and calibration IDs and attempts to calibrate gaze.
    "   Returns the participant ID for recording."""

    # Create socket which will send a keep alive message for the live data stream
    data_gsocket = mkgsock(glasses_ip)
    peer = (glasses_ip, port)
    keepalive = KeepAlive(data_gsocket, peer, KA_DATA_MSG)
    base_url = 'http://' + str(glasses_ip)

    project_id = create_project(base_url)
    participant_id = create_participant(base_url, project_id)
    calibration_id = create_calibration(base_url, project_id, participant_id)

    print("Project: " + project_id + " Participant: " + participant_id +
          " Calibration: " + calibration_id)

    print('Starting calibration ...')
    start_calibration(calibration_id, base_url)
    status = wait_for_status(base_url,
                             '/api/calibrations/' + calibration_id + '/status',
                             'ca_state', ['failed', 'calibrated'])
    # Clean up: Close gsocket and stop keep alive messages
    stop_calibration(data_gsocket, keepalive)
    return participant_id, status