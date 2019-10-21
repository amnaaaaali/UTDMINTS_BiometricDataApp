- Tested with Python 3.7 on Windows 10 and MSYS2 (64bit ver)
- Need to intall and run on MSYS2.
- To execute file: python3 livestream_data_video_p3.py

Resources:
- MSYS2 installer: https://www.msys2.org
 	> Documentation: https://github.com/msys2/msys2
	> installing packages in MSYS2: https://github.com/msys2/msys2/wiki/Using-packages
	> packages required: (see below)
	> error with opencv 4.1.1 need 4.1.0
		>> use file: mingw-w64-x86_64-opencv-4.1.0-3-any.pkg.tar.xz
		>> cmd in msys2: 
			pacman -U mingw-w64-x86_64-opencv-4.1.0-3-any.pkg.tar.xz
			

- Gstreamer: https://gstreamer.freedesktop.org/documentation/?gi-language=c

- PyGobject API Reference: https://lazka.github.io/pgi-docs/index.html

- packages: (windows ver)
	mingw64/mingw-w64-x86_64-gstreamer 1.16.0-2
	mingw-w64-x86_64-gst-libav 1.16.0-3
	mingw-w64-x86_64-gst-plugins-bad 1.16.0-3
	mingw-w64-x86_64-gst-plugins-base 1.16.0-3
	mingw-w64-x86_64-gst-plugins-good 1.16.0-2
	mingw-w64-x86_64-gst-python 1.16.0-2
	mingw-w64-x86_64-gtk3 3.24.10-3
	mingw-w64-x86_64-python3 3.7.4-7
	mingw-w64-x86_64-python3-gobject 3.32.2-1
