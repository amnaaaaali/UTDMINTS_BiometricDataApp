- Tested with Python 3.7 on Windows 10(64 bit) and MSYS2 (64bit ver)
- Need to intall and run on MSYS2.
- To execute file: python3 livestream_data_video_p3.py

Resources:
- MSYS2 installer: https://www.msys2.org
 	> Documentation: https://github.com/msys2/msys2
	> installing packages in MSYS2: https://github.com/msys2/msys2/wiki/Using-packages
		>> cmd: pacman -S <package name>
	> package repo for older version: http://repo.msys2.org/mingw/x86_64/
		1. copy file into  msys64/home/user/ directory
		2. install packages using: pacman -U <filename>
	> error with opencv 4.1.1 use 4.1.0
		>> use file: mingw-w64-x86_64-opencv-4.1.0-3-any.pkg.tar.xz
		>> cmd in msys2: 
			pacman -U mingw-w64-x86_64-opencv-4.1.0-3-any.pkg.tar.xz			

- Gstreamer: 
	https://gstreamer.freedesktop.org/documentation/?gi-language=c

- Windows Installation for PyGObject: 
	https://pygobject.readthedocs.io/en/latest/getting_started.html#windows-getting-started

- PyGobject API Reference: 
	https://lazka.github.io/pgi-docs/index.html

- packages required:
	mingw-w64-x86_64-gstreamer 1.16.0-2
	mingw-w64-x86_64-gst-libav 1.16.0-3
	mingw-w64-x86_64-gst-plugins-bad 1.16.0-3
	mingw-w64-x86_64-gst-plugins-base 1.16.0-3
	mingw-w64-x86_64-gst-plugins-good 1.16.0-2
	mingw-w64-x86_64-gst-python 1.16.0-2
	mingw-w64-x86_64-gtk3 3.24.10-3
	mingw-w64-x86_64-python3 3.7.4-7
	mingw-w64-x86_64-python3-gobject 3.32.2-1
	mingw-w64-x86_64-pygobject-devel 3.32.2-1
	mingw-w64-x86_64-opencv 4.1.0-3
	mingw-w64-x86_64-twolame 0.3.13-3
	
