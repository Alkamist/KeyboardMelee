import time

from state import State
from delayed_state import DelayedState
from button_axis import ButtonAxis


class BStick(object):
    def __init__(self):
        self.b_state = DelayedState(delay=0.0, minimum_hold_time=0.025)
        self.x_axis_output = 0.0
        self.y_axis_output = 0.0

        self._x_axis = ButtonAxis()
        self._y_axis = ButtonAxis()
        self._b_neutral = DelayedState(delay=0.0, minimum_hold_time=0.034)
        self._b_left = DelayedState(delay=0.0, minimum_hold_time=0.034)
        self._b_right = DelayedState(delay=0.0, minimum_hold_time=0.034)
        self._b_down = DelayedState(delay=0.0, minimum_hold_time=0.034)
        self._b_up = DelayedState(delay=0.0, minimum_hold_time=0.050)
        self._activation_time = 0.0
        self._axis_hold_duration = 0.050

    def update(self, b_neutral, b_left, b_right, b_down, b_up, ls_x_raw, ls_x, ls_y):
        self.x_axis_output = ls_x
        self.y_axis_output = ls_y

        self._update_inputs(b_neutral, b_left, b_right, b_down, b_up)

        # Delay the b press by one frame if doing up b.
        if self._b_up.just_activated:
            self._activation_time = time.perf_counter()
            self.b_state.delay = 0.017
            self._axis_hold_duration = 0.050

        if self._b_down.just_activated \
        or self._b_left.just_activated \
        or self._b_right.just_activated:
            self._activation_time = time.perf_counter()
            self.b_state.delay = 0.0
            self._axis_hold_duration = 0.050

        if self._b_neutral.just_activated:
            self._activation_time = time.perf_counter()
            self.b_state.delay = 0.0
            self._axis_hold_duration = 0.025

        self.b_state.is_active = self._b_neutral.is_active \
                              or self._b_left.is_active or self._b_right.is_active \
                              or self._b_down.is_active or self._b_up.is_active

        self._x_axis.update(self._b_left.is_active, self._b_right.is_active)
        self._y_axis.update(self._b_down.is_active, self._b_up.is_active)

        if time.perf_counter() - self._activation_time <= self._axis_hold_duration:
            should_bias_x = self._b_down.is_active or self._b_up.is_active or (ls_x_raw != 0.0 and self._b_neutral.is_active)
            x_bias = 0.2875 * ls_x_raw if should_bias_x else 0.0
            self.x_axis_output = self._x_axis.value + x_bias
            self.y_axis_output = self._y_axis.value * 0.6 if self._y_axis.value < 0.0 else self._y_axis.value

        self.b_state.update()

    def _update_inputs(self, b_neutral, b_left, b_right, b_down, b_up):
        self._b_neutral.is_active = b_neutral
        self._b_left.is_active = b_left
        self._b_right.is_active = b_right
        self._b_down.is_active = b_down
        self._b_up.is_active = b_up
        self._b_neutral.update()
        self._b_left.update()
        self._b_right.update()
        self._b_down.update()
        self._b_up.update()
