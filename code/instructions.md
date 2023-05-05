# Mind's Eye

The prototype camera uses a Raspberry Pi board with Raspberry Pi OS Buster.
The version of the OS with the window manager installed is needed to run the camera preview. However, if the preview isn't necessary, the headless version can be used. I haven't tried, but since the Picamera (original) library sends the camera's preview directly to the GPU output, the camera preview may work on the headless version, so long as the type of preview opened doesn't rely on QT.

---

## Autostarting camerarun.py

When the Pi boots and the window manager starts, the window manager runs camerarun.py.
To make that happen:

  $~ sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

and add at the bottom of that file:

  @lxterminal --command python /home/[your username]/camerarun.py

Now if you restart the Pi, camerarun.py should run automatically.

---

