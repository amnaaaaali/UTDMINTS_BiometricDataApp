""" Tobii UI
 " Simple UI to discover, callibrate, record and display video with gaze
 " for  the Tobii Pro 2 eye tracking glasses.
 " Must manually connect to the glasses via wifi before executing.
 " Tested with Python 3.7, Windows 10 and MSYS2 64-bit
 " Execute in MSYS2 using: python3 video_UI.py
 " successful as of 11/6/19
"""
import sys
import discover
import video_gaze
import calibrate
import record
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, Gio, GLib

PORT = 49152
OPTIONS = [
    "Press 'c' to Calibrate.",
    "Press 'r' to Record. Requires calibration first.",
    "Press 's' to Stop recording. Recording must be already in progress",
    "Press 'q' to Quit."
]


# using class to avoid using global variables with threads
class UIData:
    """Tracks calibration and recording progress"""
    def __init__(self):
        self.is_Calibrated = False
        self.is_Recording = False
        self.glasses_IP = ""
        self.participant_ID = ""
        self.recording_ID = ""

    def calibrated(self):
        self.is_Calibrated = True

    def recording(self):
        self.is_Recording = True


def stdin_callback(ioc, cond, ui):
    """ Get user input after entering main loop context"""
    line = ioc.read_line()[1]
    input_char = line[0]
    if input_char == 'o':
        display_options()
    # Calibrate
    elif input_char == 'c':
        # Only calibrate if not already calibrated
        if ui.is_Calibrated:
            print("Calibration arleady done. Ready to record.")
        else:
            ui.participant_ID = calibrate.calibrate(ui.glasses_IP, PORT)
            ui.calibrated()
            print("Particpant ID: " + ui.participant_ID)
    # Quit
    elif input_char == 'q':
        print("Stopping Video...")
        video.stop()
        print("Stopping Eyetracking ...")
        et.stop()
        ml.quit()
    # Record
    elif input_char == 'r':
        # Calibration required first
        if ui.is_Calibrated:
            ui.recording_ID = record.start_recording(ui.glasses_IP,
                                                     ui.participant_ID)
            ui.recording()
        else:
            print("Calibration required before recording.")
    # Stop Recording
    elif input_char == 's':
        # check if recording is in progress
        if ui.is_Recording:
            record.stop_recording(ui.glasses_IP, ui.recording_ID)
            # Update user interface data
            ui.is_Recording = False
            ui.is_Calibrated = False
        else:
            print("No recording in progress.")
    return True


def display_options():
    print("Options:")
    for opt in OPTIONS:
        print(opt)


if __name__ == '__main__':
    # data to be passed to callback
    ui_data = UIData()
    # Discover glasses
    input_var = input("Press enter to discover Tobii glasses.\n")
    glasses_IP = discover.discover()
    #print("Glasses IP:" + glasses_IP) #test

    ui_data.glasses_IP = glasses_IP

    intput_var = input("Press enter to start video with gaze.")
    #video_gaze.run(glasses_IP, PORT)
    Gst.init(None)
    ml = GLib.MainLoop()

    # Create IOChannel for user input
    stdin_ioc = GLib.IOChannel.win32_new_fd(sys.stdin.fileno())
    # Add to main loop context
    stdin_ioc_sig = GLib.io_add_watch(stdin_ioc, GLib.IO_IN, stdin_callback,
                                      ui_data)

    peer = (glasses_IP, PORT)
    # Create Video and Gaze and BufferSync
    video = video_gaze.Video()
    et = video_gaze.EyeTracking()
    buffersync = video_gaze.BufferSync(video.draw_gaze)
    # Start video and gaze
    print("Initilializing eye tracking ...")
    et.start(peer, buffersync)
    print("Initializing video ...")
    video.start(peer, buffersync)
    print("Running ... Press o at anytime for list of options.")

    # Enter main loop
    ml.run()
    # Returns here after quit is called
    GLib.source_remove(stdin_ioc_sig)

    print("Good-Bye.")
