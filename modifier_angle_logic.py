import time


class ModifierAngleLogic(object):
    def __init__(self):
        self.x_axis_output = 0.0
        self.y_axis_output = 0.0
        self._y_mod_x = 0.9500
        self._y_mod_y = 0.2875
        self._x_mod_x = 0.2875
        self._x_mod_y = 0.9500

    def update(self, x_mod, y_mod, ls_x_raw, ls_y_raw, ls_x, ls_y):
        if y_mod:
            self.x_axis_output = ls_x_raw * self._y_mod_x
            self.y_axis_output = ls_y_raw * self._y_mod_y
        elif x_mod:
            self.x_axis_output = ls_x_raw * self._x_mod_x
            self.y_axis_output = ls_y_raw * self._x_mod_y
        else:
            self.x_axis_output = ls_x
            self.y_axis_output = ls_y
