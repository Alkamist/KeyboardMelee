import time

from state import State


class SafeGroundedDownBLogic(object):
    def __init__(self):
        self.x_axis_output = 0.0
        self.y_axis_output = 0.0

        self._is_doing_safe_b = False
        self._safe_b_time = 0.0
        self._x_level = 0.5875
        self._y_level = 0.6000
        self._b_state = State()

    def update(self, b, down, up, ls_x_raw, ls_y_raw, ls_x, ls_y):
        self._b_state.is_active = b
        self._b_state.update()

        if self._b_state.just_activated and (down or up):
            self._is_doing_safe_b = True
            self._safe_b_time = time.perf_counter()

        if self._is_doing_safe_b:
            if time.perf_counter() - self._safe_b_time < 0.025:
                self.x_axis_output = ls_x_raw * self._x_level
                self.y_axis_output = ls_y_raw * self._y_level
            else:
                self._is_doing_safe_b = False
        else:
            self.x_axis_output = ls_x
            self.y_axis_output = ls_y