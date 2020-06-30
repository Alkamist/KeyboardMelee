import time

from state import State


class WavelandAngleManager(object):
    def __init__(self):
        self.x_value = 0.0
        self.y_value = 0.0
        self.x_level = 0.9375
        self.y_level = -0.3125
        self.air_dodge_state = State()
        self.is_wavelanding = False
        self.waveland_time = 0.0

    def update(self, air_dodge, left, right, down, x_axis_value, y_axis_value):
        self.air_dodge_state.update()
        self.air_dodge_state.is_active = air_dodge

        self.x_value = x_axis_value
        self.y_value = y_axis_value

        waveland_sideways = (left or right) and not down

        if self.air_dodge_state.just_activated:
            self.is_wavelanding = True
            self.waveland_time = time.perf_counter()

        if self.is_wavelanding and not down:
            if time.perf_counter() - self.waveland_time < 0.025:
                if waveland_sideways:
                    self.x_value = x_axis_value * self.x_level
                    self.y_value = self.y_level

                else:
                    self.y_value = -1.0

            else:
                self.is_wavelanding = False
