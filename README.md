# UTDMINTS_BiometricDataApp

## Tobii GUI

### Prerequisites

* Windows 10
* Python 3.7
* MSYS2 MINGW64 - The shell launcher to use
* Access to Tobii Pro Glasses 2

### MSYS2 Installation & Setup

* [MSYS2](https://www.msys2.org/) - The software distro and building platform used

After downloading and installing MSYS2 for 64 bit additional packages will be required:
* gstreamer 1.16.0-2
* gst-libav 1.16.0-3
* gst-plugins-bad 1.16.0-3
* gst-plugins-base 1.16.0-3
* gst-plugins-good 1.16.0-2
* python 1.16.0-2
* gtk3 3.24.10-3
* python3 3.7.4-7
* python3-gobject 3.32.2-1
* pygobject-devel 3.32.2-1
* opencv 4.1.0-3
* twolame 0.3.13-3

Launch the MSYS MINGW64 shell launcher (blue icon). To search for a package:
```
pacman -Ss pygobject-devel
```
Similiar to the following will be returned:
```
mingw32/mingw-w64-i686-pygobject-devel 3.32.2-1
    Development files for the pygobject bindings
mingw64/mingw-w64-x86_64-pygobject-devel 3.32.2-1
    Development files for the pygobject bindings
```
To install the package:
```
pacman -S mingw-w64-x86_64-pygobject-devel
```
As of Oct 2019, some of these packages have been updated and have not been tested with our project.
If the packages mentioned above are not currently available, they can be downloaded from the [x86_64 Package Repo](http://repo.msys2.org/mingw/x86_64/)

Download and copy the package the into your ../msys64/home/user/ directory
Install the downloaded package with:
```
pacman -U <packagename>
```
For example:
```
pacman -U mingw-w64-x86_64-opencv-4.1.0-3-any.pkg.tar.xz
```
Additional Instructions for packages [here](https://github.com/msys2/msys2/wiki/Using-packages).

### Execution

Simply type the following in the MSYS2 MINGW64 shell launcher to run the GUI independently

```
$ python3 tobii_gui.py
```
Module dependencies:
* discover.py
* video_gaze.py
* calibrate.py
* record.py

### Issues

Video overlay not opaque. Video is difficult to see if there are other apps or windows behind the GUI window and if the desktop background is not solid black.

### Built With

* [Gstreamer](https://gstreamer.freedesktop.org/documentation/?gi-language=c) - The multimedia framework used
* [PyGobject](https://pygobject.readthedocs.io/en/latest/index.html) - PyGObject is a Python package which provides bindings for GObject based libraries such as GTK, GStreamer, WebKitGTK, GLib, GIO and many more.

### References

* [PyGObject API Reference](https://lazka.github.io/pgi-docs/index.html)
* [MSYS2 Install Guide](https://github.com/msys2/msys2/wiki/MSYS2-installation)
* [MSYS Packages](https://packages.msys2.org/updates)
* [Tobii Pro SDK Documentation](http://developer.tobiipro.com/)


## EEG Plots

#### AlphaFrequencies.py, DeltaFrequencies.py, ThetaFrequencies.py
Each file shows each of the different Alpha, Delta, and Theta bands' EEG plots in
seperate plots


#### MultiFrequencies.py
All 3 frequency bands, Alpha, Delta and Theta bands' plots are shown in one figure
in this file. 


#### MultiZscore.py
All 3 frequency bands are shown with their Zscores plotted instead of the powers as with
the other files.

#### Z_Scores_ByFreq.py
This file shows each of the different Alpha, Delta, and Theta bands' EEG plots in three separate plots
in one window.

How to Run The Code:
Run SendData3.py and then run Z_Scores_ByFreq.py visualization simultaneously. SendData3.py has code that has been previously recorded via a Python Lab Streaming Layer (PyLSL) outlet.


#### GetCmapValues.py
getCmapByFreqVal: For a given frequency value, the function calls the fourier transform on the current
sample of data and computes the cmap value for that sample of data based on the power value.
getCmapForZscores: Exactly the same as getCmapByFreqVal but computes the zscore value and uses
that in the cmap.

