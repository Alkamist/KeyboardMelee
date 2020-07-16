# Keyboard Melee

This is a Python script I wrote for Windows that is designed to allow quick and controlled gameplay of Super Smash Bros. Melee on the keyboard. It works by getting your input from the keyboard, processing it, and sending the result to a third party driver called [vJoy](http://vjoystick.sourceforge.net/site/index.php/download-a-install/download). This simulates a gamepad that is visible to the Dolphin emulator.

My goal with this project was to try to create the most intuitive digital control scheme I could possibly think of to play platform fighters. While, in my opinion, there is nothing truly game breaking about what I've done, I have had to facilitate some of the intuitive feel behind the controller with the use of very simple macros. Most purists would probably vote for this to not be tournament legal, but I didn't make this script with that as a concern.

This is mainly designed as a study of how digital control schemes can work with platform fighters, and as a gateway for experimentation in this regard without having to invest in expensive specialized hardware.

Note that if you are not using a mechanical keyboard, you will likely run into issues with not having [n-key rollover](https://en.wikipedia.org/wiki/Rollover_(key)).

## Installation

- Install [Python](https://www.python.org/).
- Install [vJoy](http://vjoystick.sourceforge.net/site/index.php/download-a-install/download).
- Do a Windows search for "Configure vJoy", which will open up a program. In that program, set the number of buttons to 12, and make sure all of the Axes checkboxes are ticked. Also ensure that "Enable vJoy" is ticked at the bottom left.
- Download the .zip of this repository from the top of this page, by clicking on the "Code" dropdown menu, and selecting "Download ZIP".
- Unzip the contents to a folder wherever you want, and navigate to "Program Files\vJoy\x64". Copy "vJoyInterface.dll" to the folder that you unzipped.
- You can now run the script by either double clicking the "run.bat" file in the folder you unzipped, or by navigating to that folder in a command line and typing "python run.py" without the quotes.
- If you haven't done so already, install [Dolphin](https://slippi.gg/). You also need an SSBM ISO.
- In the Dolphin controller configuration, select "Standard Controller" in the port of your choice.
- Click the "Configure" box next to the port and load the "B0XX" profile, that should be present in the dropdown menu to the right side of the window.
- In the "Device" dropdown menu to the left side of the window, be sure to select the vJoy device, which probably looks something like "DInput/0/vJoy Device".
- You should now be ready to play Melee with the keyboard as long as the python script is running!

## Tutorial

Your left hand should be rooted on WASD, as with most games. Those keys will control the virtual control stick as expected. Your left pinky should be on Caps Lock. Holding Caps Lock will force the virtual control stick to move slowly enough to allow for walking, turning around, holding up without tap jumping, etc.

Your right hand should be rooted with your index finger on the ; key, your middle finger on the [ key, your ring finger on the ] key, and your pinky on the \\ key. Your right thumb should be rooted on Right Alt. Note that this is what works with my keyboard, and might not be comfortable with yours, so you may have to experiment with rebinding some keys to suit your needs.

The bulk of the tutorial is probably best described by explaining how to perform various techniques.

- **Short Hop**: Use your middle finger to press the [ key.
- **Full Hop**: Use your pinky to press the \\ key.
- **L-Cancel**: Use your ring finger to press the ] key.
- **Shield**: Use your ring finger to hold the ] key.
- **Light Shield**: Press Tab while holding Shield to toggle Light Shield.
- **Wavedash**: Jump with your middle finger on the [ key, and then use your right thumb to press Right Alt while holding a direction with WASD. Holding A or D will result in a max distance wavedash in the respective direction. Holding diagonally downward with WASD will result in a shorter wavedash. Holding Caps Lock while doing a wavedash will shorten the distance. Holding no direction will result in a wavedash straight downward.
- **Grab**: Use your ring finger to press the Enter key.
- **Up Smash/Up Aerial**: Use your index finger to press the P Key.
- **Left Smash/Left Aerial**: Use your index finger to press the L Key, use S or W to angle it.
- **Right Smash/Right Aerial**: Use your index finger to press the / Key, use S or W to angle it.
- **Down Smash/Down Aerial**: Use your index finger to press the ' Key.
- **Jab/Neutral Aerial**: Use your right thumb to press the Right Windows Key. Note that if you don't have a Right Windows key on your keyboard, you might need to do some button rebinds to put this somewhere else.
- **Up Tilt**: Hold Caps Lock and use your right index finger to press the P key.
- **Left Tilt**: Hold Caps Lock and use your right index finger to press the L key, use S or W to angle it.
- **Right Tilt**: Hold Caps Lock and use your right index finger to press the / key, use S or W to angle it.
- **Down Tilt**: Hold Caps Lock and use your right index finger to press the ' key.
- **Neutral B**: Use your index finger to press the . key.
- **Up B**: Use your ring finger or pinky to press the Backspace key.
- **Left B**: Use your middle finger to press the - key.
- **Right B**: Use your middle finger to press the = key.
- **Down B**: Use your index finger to press the ; key.
- **Toggle Script**: Press the 8 key.
- **Start**: Press the 5 key.
- **D Pad**: Use the G, V, B, and N keys.
- **Stick Angles**: I haven't fully worked out what I want to do with this, but for now, Space Bar and Left Alt will modify the angles made with WASD to allow for the steepest and most shallow angles.

## Issues

- The script should block the keys it is using along with some others while it is running, however there are some annoying consequences of using the Right Windows key. Blocking that key doesn't seem to block some Windows shortcuts, and there is one in particular that is super annoying, which is Windows + L, which will log you out of your PC. You can disable this shortcut with a [registry edit](https://www.howtogeek.com/howto/windows-vista/disableenable-lock-workstation-functionality-windows-l/).
- You should probably have the script running before booting up Dolphin so the controller calibrates correctly. If you are having problems light shielding this is probably because the controller did not calibrate correctly.
- The script might sometimes complain that Right Alt is an unknown key. If this happens, keep trying to run the script until it stops complaining. If you can't get it to stop, try deleting the "__ pycache__" folder in the directory. I have no idea why this happens and I haven't been able to figure out a fix for it.


