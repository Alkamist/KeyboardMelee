import time

from state import State
from delayed_state import DelayedState
from button_axis import ButtonAxis


class AStick(object):
    def __init__(self):
        self.a_state = DelayedState(delay=0.0, minimum_hold_time=0.025)
        self.x_axis_output = 0.0
        self.y_axis_output = 0.0

        self._x_axis = ButtonAxis()
        self._y_axis = ButtonAxis()
        self._a_neutral = DelayedState(delay=0.0, minimum_hold_time=0.034)
        self._a_left = DelayedState(delay=0.0, minimum_hold_time=0.050)
        self._a_right = DelayedState(delay=0.0, minimum_hold_time=0.050)
        self._a_down = DelayedState(delay=0.0, minimum_hold_time=0.034)
        self._a_up = DelayedState(delay=0.0, minimum_hold_time=0.034)
        self._activation_time = 0.0
        self._axis_hold_duration = 0.067

    def update(self, a_neutral, a_left, a_right, a_down, a_up, ls_x_raw, ls_y_raw, ls_x, ls_y):
        self.x_axis_output = ls_x
        self.y_axis_output = ls_y

        self._update_inputs(a_neutral, a_left, a_right, a_down, a_up)

        if self._a_left.just_activated and ls_x_raw > 0.0 \
        or self._a_right.just_activated and ls_x_raw < 0.0:
            self._activation_time = time.perf_counter()
            self.a_state.delay = 0.034
            self._axis_hold_duration = 0.067
        elif self._a_left.just_activated or self._a_right.just_activated:
            self._activation_time = time.perf_counter()
            self.a_state.delay = 0.017
            self._axis_hold_duration = 0.067

        if self._a_up.just_activated \
        or self._a_down.just_activated:
            self._activation_time = time.perf_counter()
            self.a_state.delay = 0.0
            self._axis_hold_duration = 0.067

        if self._a_neutral.just_activated:
            self._activation_time = time.perf_counter()
            self.a_state.delay = 0.0
            self._axis_hold_duration = 0.025

        self.a_state.is_active = self._a_neutral.is_active \
                              or self._a_left.is_active or self._a_right.is_active \
                              or self._a_down.is_active or self._a_up.is_active

        self._x_axis.update(self._a_left.is_active, self._a_right.is_active)
        self._y_axis.update(self._a_down.is_active, self._a_up.is_active)

        if time.perf_counter() - self._activation_time <= self._axis_hold_duration:
            should_bias_x = not (self._a_left.is_active or self._a_right.is_active or self._a_neutral.is_active)
            x_bias = 0.35 * ls_x_raw if should_bias_x else 0.0
            self.x_axis_output = self._x_axis.value * 0.6 + x_bias

            should_bias_y = not (self._a_down.is_active or self._a_up.is_active or self._a_neutral.is_active) and ls_y_raw != 0.0
            y_bias = 0.5 * ls_y_raw if should_bias_y else 0.0
            self.y_axis_output = self._y_axis.value * 0.6 + y_bias

        self.a_state.update()

    def _update_inputs(self, a_neutral, a_left, a_right, a_down, a_up):
        self._a_neutral.is_active = a_neutral
        self._a_left.is_active = a_left
        self._a_right.is_active = a_right
        self._a_down.is_active = a_down
        self._a_up.is_active = a_up
        self._a_neutral.update()
        self._a_left.update()
        self._a_right.update()
        self._a_down.update()
        self._a_up.update()

