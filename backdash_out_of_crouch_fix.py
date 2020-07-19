import time

from state import State


class BackdashOutOfCrouchFix(object):
    def __init__(self):
        self.x_axis_output = 0.0

        self._backdash_time = 0.0
        self._delay_backdash = False
        self._down_state = State()
        self._left_state = State()
        self._right_state = State()

    def update(self, down, left, right, tilt, ls_x):
        self._down_state.is_active = down
        self._left_state.is_active = left
        self._right_state.is_active = right

        self._down_state.update()
        self._left_state.update()
        self._right_state.update()

        if self._down_state.is_active and (self._left_state.just_activated or self._right_state.just_activated) and not tilt:
            self._delay_backdash = True
            self._backdash_time = time.perf_counter()

        if self._down_state.just_deactivated:
            self._delay_backdash = False

        if self._delay_backdash:
            self.x_axis_output = 0.0
            if time.perf_counter() - self._backdash_time >= 0.035:
                self._delay_backdash = False
        else:
            self.x_axis_output = ls_x
