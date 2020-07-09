import sys
from pathlib import Path
from ctypes import *
from ctypes import wintypes


DLL_PATH = Path.cwd().joinpath("vJoyInterface.dll")

vJoy = cdll.LoadLibrary(str(DLL_PATH))

try:
	vJoy = cdll.LoadLibrary(str(DLL_PATH))
except OSError:
	sys.exit("Unable to load vJoy SDK DLL.  Ensure that %s is present" % DLL_PATH)


axes = {
    "x" : "wAxisX",
    "y" : "wAxisY",
    "z" : "wAxisZ",
    "rx" :"wAxisXRot",
    "ry" : "wAxisYRot",
    #"rz" : "wAxisZRot",
    "sl0" : "wSlider",
    #"sl1" : 0x37,
}


class VJoyState(Structure):
    _fields_ = [
        ("bDevice", c_byte),
        ("wThrottle", c_long),
        ("wRudder", c_long),
        ("wAileron", c_long),
        ("wAxisX", c_long),
        ("wAxisY", c_long),
        ("wAxisZ", c_long),
        ("wAxisXRot", c_long),
        ("wAxisYRot", c_long),
        ("wAxisZRot", c_long),
        ("wSlider", c_long),
        ("wDial", c_long),
        ("wWheel", c_long),
        ("wAxisVX", c_long),
        ("wAxisVY", c_long),
        ("wAxisVZ", c_long),
        ("wAxisVBRX", c_long),
        ("wAxisVRBY", c_long),
        ("wAxisVRBZ", c_long),

        ("lButtons", c_long), # 32 buttons: 0x00000001 means button1 is pressed, 0x80000000 -> button32 is pressed

        ("bHats", wintypes.DWORD), # Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
        ("bHatsEx1", wintypes.DWORD), # Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
        ("bHatsEx2", wintypes.DWORD), # Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
        ("bHatsEx3", wintypes.DWORD), # Lower 4 bits: HAT switch or 16-bit of continuous HAT switch LONG lButtonsEx1

        ("lButtonsEx1", c_long), # Buttons 33-64
        ("lButtonsEx2", c_long), # Buttons 65-96
        ("lButtonsEx3", c_long), # Buttons 97-128
    ]

    def __init__(self, device_id):
        self.bDevice = c_byte(device_id)
        self.bHats = -1


class VJoyDevice(object):
    def __init__(self, device_id):
        self.device_id = device_id
        self.data = VJoyState(self.device_id)

        try:
            vJoy.vJoyEnabled()
            vJoy.AcquireVJD(device_id)
        except:
            sys.exit("vJoy is not enabled on this system.")

    def set_button(self, button_id, state):
        bit_index = button_id - 1
        if state:
            self.data.lButtons = self.data.lButtons | (1 << bit_index)
        else:
            self.data.lButtons = self.data.lButtons & ~(1 << bit_index)

    def set_axis(self, axis_name, value):
        scaled_value = int(value * 0x8000)
        setattr(self.data, axes[axis_name], scaled_value)

    def update(self):
        vJoy.UpdateVJD(self.device_id, self.data)

    def __del__(self):
        vJoy.RelinquishVJD(self.device_id)
