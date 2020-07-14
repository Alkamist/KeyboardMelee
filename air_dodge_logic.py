import time

from state import State


class AirDodgeLogic(object):
    def __init__(self):
        self.x_axis_output = 0.0
        self.y_axis_output = 0.0
        self.x_level_long = 0.9375
        self.y_level_long = -0.3125
        self.x_level_medium = 0.8125
        self.y_level_medium = -0.5750
        self.x_level_short = 0.5000
        self.y_level_short = -0.8500
        self._is_air_dodging = False
        self._air_dodge_time = 0.0
        self._air_dodge_state = State()

    def update(self, air_dodge, tilt, left, right, down, up, ls_x_raw, ls_x, ls_y):
        self.x_axis_output = ls_x
        self.y_axis_output = ls_y

        self._air_dodge_state.is_active = air_dodge
        self._air_dodge_state.update()

        sideways = (left or right) and not down
        diagonal = (left or right) and (down or up)

        waveland_short = diagonal and tilt
        waveland_medium = sideways and tilt
        waveland_long = sideways and not tilt

        if self._air_dodge_state.just_activated:
            self._is_air_dodging = True
            self._air_dodge_time = time.perf_counter()

        if self._is_air_dodging and not up:
            if time.perf_counter() - self._air_dodge_time < 0.051:
                if waveland_long:
                    self.x_axis_output = ls_x_raw * self.x_level_long
                    self.y_axis_output = self.y_level_long

                elif waveland_medium:
                    self.x_axis_output = ls_x_raw * self.x_level_medium
                    self.y_axis_output = self.y_level_medium

                elif waveland_short:
                    self.x_axis_output = ls_x_raw * self.x_level_short
                    self.y_axis_output = self.y_level_short

                elif not down:
                    self.y_axis_output = -0.3

            else:
                self._is_air_dodging = False
