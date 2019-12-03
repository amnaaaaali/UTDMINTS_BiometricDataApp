import discover
import video_gaze as vg
import calibrate as calibrate
import record as record
import ctypes
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst

X_POS = 1000
Y_POS = 500
BORDER_WIDTH = 6
BOX_SPACING = 6
MAX_HEIGHT = 356
MAX_WIDTH = 584

PORT = 49152


# Sub-class Gtk.Window to define our own classs
class Tobii_GUI():
    def __init__(self):
        # Initilize GTK
        Gtk.init(None)
        #Initialize Gst
        Gst.init(None)
        self.is_Calibrated = False
        self.is_Recording = False
        self.is_Discovered = False
        self.glasses_ip = ""
        self.participant_id = ""
        self.recording_id = ""
        self.video = None
        self.video_window_handle = None
        self.eye_tracking = None
        self.buffersync = None
        self.build_ui()

    def build_ui(self):
        # Set up main window to hold all components
        main_window = Gtk.Window.new(Gtk.WindowType.TOPLEVEL)
        main_window.set_title("Tobii Video")
        main_window.set_border_width(BORDER_WIDTH)
        #main_window.set_resizable(False)
        main_window.set_default_size(MAX_WIDTH, MAX_HEIGHT)
        # Handles event when 'x' button clicked to close window
        main_window.connect("delete-event", self.on_delete_event)

        # Create video window
        video_window = Gtk.DrawingArea()
        video_window.connect("realize", self.on_realize)

        # Create Control buttons and connect to click events
        btn_Discover = Gtk.Button(label="Discover")
        btn_Discover.connect("clicked", self.on_discover)

        btn_Calibrate = Gtk.Button(label="Calibrate")
        btn_Calibrate.connect("clicked", self.on_calibrate)

        btn_Start_Record = Gtk.Button.new_from_icon_name(
            "media-record", Gtk.IconSize.BUTTON)
        btn_Start_Record.connect("clicked", self.on_start_record)

        btn_Stop_Record = Gtk.Button.new_from_icon_name(
            "media-playback-stop", Gtk.IconSize.BUTTON)
        btn_Stop_Record.connect("clicked", self.on_stop_record)

        # Create box to hold buttons
        controls = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                           spacing=BOX_SPACING)

        # Add buttons to control box
        controls.pack_start(btn_Discover, True, True, 0)
        controls.pack_start(btn_Calibrate, True, True, 0)
        controls.pack_start(btn_Start_Record, True, True, 0)
        controls.pack_start(btn_Stop_Record, True, True, 0)

        # Create box to contain video and controls
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                           spacing=BOX_SPACING)
        main_box.pack_start(video_window, True, True, 0)
        main_box.pack_start(controls, False, False, 0)

        main_window.add(main_box)

        # Specify window position
        main_window.move(X_POS, Y_POS)
        # Display window and all it's components
        main_window.show_all()

    # Start Gtk main loop
    def start(self):
        Gtk.main()

    # Terminate if we click on x to close window
    def on_delete_event(self, widget, event):
        if self.video is not None:
            self.video.stop()
        if self.eye_tracking is not None:
            self.eye_tracking.stop()
        Gtk.main_quit()

    def on_discover(self, widget):
        # Discovers the glasses via ethernet.
        # Glasses must be connected before discovering
        if self.is_Discovered:
            print("Glasses already discovered. Not action required.")
        else:
            self.glasses_ip = discover.discover()
            if not self.glasses_ip:
                print("Glasses not found")
            else:
                print("Glasses found")
                self.is_Discovered = True
                #Start video
                peer = (self.glasses_ip, PORT)
                # Create Video, Eye Tracking and BufferSync
                self.video = vg.Video()
                self.eye_tracking = vg.EyeTracking()
                self.buffersync = vg.BufferSync(self.video.draw_gaze)
                # Start eyetracking and video
                print("Initializing eye tracking ...")
                self.eye_tracking.start(peer, self.buffersync)
                print("Starting video ...")
                self.video.start(peer, self.buffersync,
                                 self.video_window_handle)

    def on_calibrate(self, widget):
        # Calibrates video gaze if its hasn't been done already.
        # If calibration not successful, user can try again
        # or use default calibration instead.
        if self.is_Calibrated:
            # Create information dialog box
            dialog = Gtk.MessageDialog(
                parent=None,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Glasses already calibrated. Ready to record.")
            # Launch dialog box
            dialog.run()
            dialog.destroy()
        else:
            print("Calibrating video gaze ...")
            self.participant_id, status = calibrate.calibrate(
                self.glasses_ip, PORT)
            if status == 'failed':
                dialog = Gtk.MessageDialog(
                    parent=None,
                    flags=0,
                    message_type=Gtk.MessageType.WARNING,
                    buttons=Gtk.ButtonsType.OK_CANCEL,
                    text="Calibration Failed")
                dialog.format_secondary_text(
                    "Using default calibration instead. Press 'ok' to continue or 'cancel' to try again."
                )
                response = dialog.run()
                if response == Gtk.ResponseType.OK:
                    self.is_Calibrated = True
                elif response == Gtk.ResponseType.CANCEL:
                    self.participant_id = ""
                    self.is_Calibrated = False
                dialog.destroy()
            else:
                self.is_Calibrated = True
                dialog = Gtk.MessageDialog(parent=None,
                                           flags=0,
                                           message_type=Gtk.MessageType.INFO,
                                           buttons=Gtk.ButtonsType.OK,
                                           text="Calibration Successful")
                dialog.run()
                dialog.destory()

    def on_start_record(self, widget):
        # Starts recording video, requires calibration first.
        if not self.is_Calibrated:
            # Create information dialog box
            dialog = Gtk.MessageDialog(
                parent=None,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Calibration required before recording.")
            # Launch dialog box
            dialog.run()
            dialog.destroy()
        elif self.is_Calibrated and not self.is_Recording:
            print("Recording starting")
            self.recording_id = record.start_recording(self.glasses_ip,
                                                       self.participant_id)
            self.is_Recording = True
        elif self.is_Recording:
            print("Recording already in progress")

    def on_stop_record(self, widget):
        # Stops recording video if one is in progress
        if self.is_Recording:
            print("Recording stopping")
            self.is_Recording = False
            self.is_Calibrated = False
        else:
            # Create information dialog box
            dialog = Gtk.MessageDialog(parent=None,
                                       flags=0,
                                       message_type=Gtk.MessageType.INFO,
                                       buttons=Gtk.ButtonsType.OK,
                                       text="No recording in progress.")
            # Launch dialog box
            dialog.run()
            dialog.destroy()

    def on_realize(self, widget):
        # Realizes window and retrieves its id for the videos's sink to render into
        window = widget.get_window()
        if not window.ensure_native():
            print("Couldn't create native window need for GstVideoOverlay")
        ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
        ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object]
        drawingArea_gpointer = ctypes.pythonapi.PyCapsule_GetPointer(
            window.__gpointer__, None)
        gdkdll = ctypes.CDLL("libgdk-3-0.dll")
        self.video_window_handle = gdkdll.gdk_win32_window_get_handle(
            drawingArea_gpointer)
        if (self.video_window_handle != 0):
            print("Window handle successfully retreived")
        else:
            print("Failed to retrieve video window handle")


if __name__ == '__main__':
    tgui = Tobii_GUI()
    tgui.start()