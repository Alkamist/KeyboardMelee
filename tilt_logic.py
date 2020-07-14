import time

from tilt_axis import TiltAxis


class TiltLogic(object):
    def __init__(self, tilt_level=0.65, minimum_active_value=0.2875):
        self.x_axis_output = 0.0
        self.y_axis_output = 0.0
        self._x_axis = TiltAxis(tilt_level, minimum_active_value)
        self._y_axis = TiltAxis(tilt_level, minimum_active_value)

    def update(self, tilt_modifier, ls_x, ls_y):
        self._x_axis.update(ls_x)
        self._y_axis.update(ls_y)

        if tilt_modifier:
            self.x_axis_output = self._x_axis.value
            self.y_axis_output = self._y_axis.value
        else:
            self.x_axis_output = ls_x
            self.y_axis_output = ls_y
