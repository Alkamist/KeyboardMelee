import sys
from pathlib import Path
from ctypes import *


DLL_PATH = Path.cwd().joinpath("vJoyInterface.dll")

vJoy = cdll.LoadLibrary(str(DLL_PATH))

try:
	vJoy = cdll.LoadLibrary(str(DLL_PATH))
except OSError:
	sys.exit("Unable to load vJoy SDK DLL.  Ensure that %s is present" % DLL_FILENAME)


axes = {
    "x" : 0x30,
    "y" : 0x31,
    "z" : 0x32,
    "rx" : 0x33,
    "ry" : 0x34,
    "rz" : 0x35,
    "sl0" : 0x36,
    "sl1" : 0x37,
}


class VJoyDevice(object):
    def __init__(self, device_id):
        self.device_id = device_id

        try:
            vJoy.vJoyEnabled()
            vJoy.AcquireVJD(device_id)
        except:
            sys.exit("vJoy is not enabled on this system.")

    def set_button(self, button_id, state):
        return vJoy.SetBtn(state, self.device_id, button_id)

    def set_axis(self, axis_name, value):
        scaled_value = int(value * 0x8000)
        return vJoy.SetAxis(scaled_value, self.device_id, axes[axis_name])

    #def set_discrete_pov(self, pov_id, value):
    #    return vJoy.SetDiscPov(value, self.device_id, pov_id)

    #def set_continuous_pov(self, pov_id, value):
    #    return vJoy.SetContPov(value, self.device_id, pov_id)

    #def reset(self):
    #    return vJoy.ResetVJD(self.device_id)

    #def reset_buttons(self):
    #    return vJoy.ResetButtons(self.device_id)

    #def reset_povs(self):
    #    return vJoy.ResetPovs(self.device_id)

    def __del__(self):
        vJoy.RelinquishVJD(self.device_id)
