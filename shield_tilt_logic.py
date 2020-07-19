import time

from tilt_stick import TiltStick


class ShieldTiltLogic(object):
    def __init__(self, shield_drop_level=0.6625, minimum_active_value=0.2875):
        self.x_axis_output = 0.0
        self.y_axis_output = 0.0

        self._tilt_stick = TiltStick(shield_drop_level, minimum_active_value, True)

    def update(self, shield, ls_x, ls_y):
        self._tilt_stick.update(shield, ls_x, ls_y)

        if shield:
            self.x_axis_output = self._tilt_stick.x_axis_output
            self.y_axis_output = self._tilt_stick.y_axis_output
        else:
            self.x_axis_output = ls_x
            self.y_axis_output = ls_y