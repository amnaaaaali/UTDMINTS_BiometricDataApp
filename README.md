# UTDMINTS_BiometricDataApp

## Tobii GUI

### Prerequisites

* Windows 10
* Python 3.7
* MSYS2 MINGW64 - The shell launcher to use

### MSYS2 Installation & Setup
* [MSYS2](https://www.msys2.org/) - The software distro and building platform used
* [Windows Installation for PyGObject](https://pygobject.readthedocs.io/en/latest/getting_started.html#windows-getting-started) - PyGObject is a Python package which provides bindings for GObject based libraries such as GTK, GStreamer, WebKitGTK, GLib, GIO and many more.

After setting up MSYS2 additional packages will be required:
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

Instructions for installing packages [here](https://github.com/msys2/msys2/wiki/MSYS2-installation).
When installing packages, ensure the prefix is 'mingw-w64-x86_64'. Version number not required.

```
$ pacman -S mingw-w64-x86_64-gstreamer
warning: mingw-w64-x86_64-gstreamer-1.16.0-2 is up to date -- reinstalling
resolving dependencies...
looking for conflicting packages...

Packages (1) mingw-w64-x86_64-gstreamer-1.16.0-2

Total Installed Size:  10.90 MiB
Net Upgrade Size:       0.00 MiB

:: Proceed with installation? [Y/n]

```

### Execution

Simply type the following in the MSYS2 MINGW64 launcher to run the GUI independently

```
$ python3 tobii_gui.py
```
### Issues

Video overlay not opaque. Video is difficult to see if there are other apps or windows behind the GUI window and if the desktop background is not solid black.

### Built With

* [Gstreamer](https://gstreamer.freedesktop.org/documentation/?gi-language=c) - The multimedia framework used

### References

* [PyGObject API Reference](https://lazka.github.io/pgi-docs/index.html)
* [x86_64 Package Repo](http://repo.msys2.org/mingw/x86_64/)


## EEG Plots
#### AlphaFrequencies.py, DeltaFrequencies.py, ThetaFrequencies.py
Each file shows each of the different Alpha, Delta, and Theta bands' EEG plots in
seperate plots


#### MultiFrequencies.py
All 3 frequency bands, Alpha, Delta and Theta bands' plots are shown in one figure
in this file. 


#### MultiZscore.py
All 3 frequency bands are shown with their Zscores plotted instead of the powers as with
the other Files


#### GetCmapValues.py
getCmapByFreqVal: For a given frequency value, the function calls the fourier transform on the current
sample of data and computes the cmap value for that sample of data based on the power value??
getCmapForZscores: Exactly the same as getCmapByFreqVal but computes the zscore value and uses
that in the cmap

