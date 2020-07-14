import time

from tilt_axis import TiltAxis


class ShieldTiltLogic(object):
    def __init__(self, shield_drop_level=0.6625, minimum_active_value=0.2875):
        self.x_axis_output = 0.0
        self.y_axis_output = 0.0
        self._x_axis = TiltAxis(shield_drop_level, minimum_active_value)
        self._y_axis = TiltAxis(shield_drop_level, minimum_active_value)

    def update(self, shield, ls_x, ls_y):
        self._x_axis.update(ls_x, shield)
        self._y_axis.update(ls_y, shield)

        if shield:
            self.x_axis_output = self._x_axis.value
            self.y_axis_output = self._y_axis.value
        else:
            self.x_axis_output = ls_x
            self.y_axis_output = ls_y