- Tested with Python 3.7 on Windows 10 and MSYS2 (64bit ver)
- Need to intall and run on MSYS2.
- To execute file: python3 livestream_data_video_p3.py

Resources:
- MSYS2 installer: https://www.msys2.org
 	> Documentation: https://github.com/msys2/msys2
	> installing packages in MSYS2: https://github.com/msys2/msys2/wiki/Using-packages
	> packages required:
		mingw64/mingw-w64-x86_64-gstreamer
		mingw64/mingw-w64-x86_64-gst-plugins-good 1.16.0-2
		mingw64/mingw-w64-x86_64-gst-plugins-bad 1.16.0-3
	> error with opencv 4.1.1 need 4.1.0
		>> use file: mingw-w64-x86_64-opencv-4.1.0-3-any.pkg.tar.xz
		>> cmd in msys2: 
			pacman -U mingw-w64-x86_64-opencv-4.1.0-3-any.pkg.tar.xz
			

- Gstreamer: https://gstreamer.freedesktop.org/documentation/?gi-language=c

- PyGobject API Reference: https://lazka.github.io/pgi-docs/index.html

- packages: 
	mingw-w64-x86_64-gst-libav
	mingw-w64-x86_64-gst-plugins-bad
	mingw-w64-x86_64-gst-plugins-base
	mingw-w64-x86_64-gst-plugins-good
	mingw-w64-x86_64-gst-plugins-ugly
	mingw-w64-x86_64-gtk3
	mingw-w64-x86_64-python3
	mingw-w64-x86_64-python3-gobject
