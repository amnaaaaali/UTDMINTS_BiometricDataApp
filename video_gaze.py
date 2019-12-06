""" Video Syncing with Gaze data overlay
"
" This example uses the video as a main source to sync eyetracking data. Since the
" video is the main source the eyetracking data will be synced on the videos output.
"
" Eyetracking data is read directly into eyetracking data queues (one sync and one data)
"
" When a video pts(presentation timestamp) is detected on the incoming data it is added with the buffer
" offset.
"
" When a video is about to be displayed its offset is matched with the offset
" in the video pts queue to get the corresponding pts. With this pts we can
" calculate the pts sync point in the eyetracking data and present the
" yetracking points that corresponds to this pts. For frames without pts we
" move eyetracking data forward using the video frame timestamps.
"
" This code does not do calibration and it does not compensate to place the
" gazepoint in the absolute center of the string "*" but rather it is the start
" of the "*" string position.
" 

TEAM TOBII NOTES:
    - Used as a module with Tobii GUI.
    - Tested with Python 3.7 on Windows 10 and MSYS2 64-bit
    - Uses gsocket and not python sockets.
    - For ethernet connection only.
    CAUTION: the following error/bug raised now and then but still runs: 
        OverflowError: Python int too large to convert to C long
        The above exception was the direct cause of the following exception:
        SystemError: PyEval_EvalFrameEx returned a result with an error set
"""

import json
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import Gst, Gio, GLib, GstVideo


def mkgsock(peer):
    """ Create a udp Gsocket pair for a peer description """
    ipfam = Gio.SocketFamily.IPV4
    if ':' in peer[0]:
        ipfam = Gio.SocketFamily.IPV6
    return Gio.Socket.new(ipfam, Gio.SocketType.DATAGRAM,
                          Gio.SocketProtocol.UDP)


class KeepAlive:
    """ Sends keep-alive signals to a peer via a gsocket """
    _sig = 0

    def __init__(self, gsock, peer, streamtype, timeout=1):
        jsonobj = json.dumps({
            'op': 'start',
            'type': ".".join(["live", streamtype, "unicast"]),
            'key': 'anything'
        })
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


class BufferSync():
    """ Handles the buffer syncing
    "
    " When new eyetracking data arrives we store it in a et (eye tracking) queue and the 
    " specific eyetracking to pts sync points in a et-pts-sync queue.
    "
    " When MPegTS is decoded we store pts values with the decoded offset in a
    " pts queue.
    "
    " When a frame is about to be displayed we take the offset and match with
    " the pts from the pts queue. This pts is then synced with the
    " et-pts-sync queue to get the current sync point. With this sync point
    " we can sync the et queue to the video output.
    "
    " For video frames without matching pts we move the eyetracking data forward
    " using the frame timestamps.
    " 
    """
    _et_syncs = []  # Eyetracking Sync items
    _et_queue = []  # Eyetracking Data items
    _et_ts = 0  # Last Eyetraing Timestamp
    _pts_queue = []  # Pts queue
    _pts_ts = 0  # Pts timestamp

    def __init__(self, cb):
        """ Initialize a Buffersync with a callback to call with each synced
        " eyetracking data
        """
        self._callback = cb

    def add_et(self, obj):
        """ Add new eyetracking data point """
        # Store sync (pts) objects in _sync queue instead of normal queue
        if 'pts' in obj:
            self._et_syncs.append(obj)
        else:
            self._et_queue.append(obj)

    def sync_et(self, pts, timestamp):
        """ Sync eyetracking sync datapoints against a video pts timestamp and stores
        " the frame timestamp
        """
        # Split the gaze syncs to ones before pts and keep the ones after pts
        syncspast = list(filter(lambda x: x['pts'] <= pts, self._et_syncs))
        self._et_syncs = list(filter(lambda x: x['pts'] > pts, self._et_syncs))
        if syncspast != []:
            # store last sync time in gaze ts and video ts
            self._et_ts = syncspast[-1]['ts']
            self._pts_ts = timestamp

    def flush_et(self, timestamp):
        """ Flushes synced eyetracking on video
        " This calculates the current timestamp with the last gaze sync and the video
        " frame timestamp issuing a callback on eyetracking data that match the
        " timestamps.
        """
        nowts = self._et_ts + (timestamp - self._pts_ts)
        # Split the eyetracking queue into passed points and future points
        passed = list(filter(lambda x: x['ts'] <= nowts, self._et_queue))
        self._et_queue = list(filter(lambda x: x['ts'] > nowts,
                                     self._et_queue))
        # Send passed to callback
        self._callback(passed)

    def add_pts_offset(self, offset, pts):
        """ Add pts to offset queue """
        self._pts_queue.append((offset, pts))

    def flush_pts(self, offset, timestamp):
        """ Flush pts to offset or use timestamp to move data forward """
        # Split pts queue to used offsets and past offsets
        used = list(filter(lambda x: x[0] <= offset, self._pts_queue))
        self._pts_queue = list(filter(lambda x: x[0] > offset,
                                      self._pts_queue))
        if used != []:
            # Sync with the last pts for this offset
            self.sync_et(used[-1][1], timestamp)
        self.flush_et(timestamp)


class EyeTracking():
    """ Read eyetracking data from the RU (recording unit)"""
    _ioc_sig = 0  #IO channel
    _buffersync = None

    def start(self, peer, buffersync):
        self._gsock = mkgsock(peer)
        self._keepalive = KeepAlive(self._gsock, peer, "data")
        ioc = GLib.IOChannel(self._gsock.get_fd())
        self._ioc_sig = GLib.io_add_watch(ioc, GLib.IO_IN, self._data)
        self._buffersync = buffersync

    def _data(self, ioc, cond):
        """ Read next line of data """
        #get 'str_return' from read_line tuple
        line = ioc.read_line()[1]
        self._buffersync.add_et(json.loads(line))
        return True

    def stop(self):
        """ Stop the live data """
        self._keepalive.stop()
        self._gsock.close()
        GLib.source_remove(self._ioc_sig)


class Video():
    """ Video stream from the RU (recording unit)"""
    _PIPEDEF = [
        "udpsrc name=src",  # UDP video data
        "tsparse",  # parse the incoming stream to MPegTS
        "tsdemux emit-stats=True",  # get pts statistics from the MPegTS stream
        "queue",  # build queue for the decoder 
        "h264parse",  # parse the stream - needs testing, may or may not need
        "avdec_h264 max-threads=0",  # decode the incoming stream to frames
        "identity name=decoded",  # used to grab video frame to be displayed
        "textoverlay name=textovl text=* halignment=position valignment=position xpad=0  ypad=0",  # simple text overlay
        "d3dvideosink force-aspect-ratio=True name=video"  # Output video   
    ]
    _pipeline = None  # The GStreamer pipeline
    _textovl = None  # Text overlay element
    _keepalive = None  # Keepalive for video
    _gsock = None  # Communicaion socket (gsocket type)

    def draw_gaze(self, objs):
        """ Move gaze point on screen """
        # Filter out gaze points. Gaze comes in higher Hz then video so there
        # should be 1 to 3 gaze points for each video frame
        objs = list(filter(lambda x: 'gp' in x, objs))
        if len(objs) > 3 or len(objs) == 0:
            return
        obj = objs[-1]
        if 'gp' in obj and obj['gp'][0] != 0 and obj['gp'][1] != 0:
            self._textovl.set_property("xpos", obj['gp'][0])
            self._textovl.set_property("ypos", obj['gp'][1])

    def start(self, peer, buffersync, video_window_handle):
        """ Start grabbing video """
        # Create socket and set syncbuffer
        self._gsock = mkgsock(peer)
        self._buffersync = buffersync

        # Create pipeline
        self._pipeline = Gst.parse_launch(" ! ".join(self._PIPEDEF))

        # Set the sink to display in the GUI window with the specified handle
        sink = self._pipeline.get_by_name("video")
        GstVideo.VideoOverlay.set_window_handle(sink, video_window_handle)

        # Add watch to pipeline to get tsdemux messages
        bus = self._pipeline.get_bus()
        bus.add_watch(GLib.PRIORITY_DEFAULT, self._bus)

        # Set socket property of udp source
        src = self._pipeline.get_by_name("src")
        src.set_property("socket", self._gsock)

        # Catch decoded frames
        decoded = self._pipeline.get_by_name("decoded")
        # Connect the handoff signal of identity element
        decoded.connect("handoff", self._decoded_buffer)

        # Store overlay object
        self._textovl = self._pipeline.get_by_name("textovl")

        # Start video streaming
        self._keepalive = KeepAlive(self._gsock, peer, "video")

        # Start the video pipeline
        self._pipeline.set_state(Gst.State.PLAYING)

    def _bus(self, bus, msg):
        """ Bus message handler 
        " Collects pts-offset pairs
        """
        if msg.type == Gst.MessageType.ELEMENT:
            st = msg.get_structure()
            # If we have a tsdemux message with pts field then lets store it
            # for the render pipeline. Will be picked up by the handoff
            if st.has_name("tsdemux") and st.has_field("pts"):
                self._buffersync.add_pts_offset(st['offset'], st['pts'])
        #return True

    def _decoded_buffer(self, ident, buf):
        """ Callback for decoded buffer """
        # Make sure to convert timestamp to us.dts = decoded timestamp
        self._buffersync.flush_pts(buf.offset, buf.dts / 1000)

    def stop(self):
        self._pipeline.set_state(Gst.State.NULL)
        self._pipeline = None
        self._gsock.close()
        self._gsock = None
        self._keepalive.stop()
        self._keepalive = None
