import time

from normalize import normalize


class WavelandAngleManager(object):
    def __init__(self):
        self.x_value = 0.0
        self.y_value = 0.0
        self.x_level_long = 0.9375
        self.y_level_long = -0.3125
        self.x_level_short = 0.5000
        self.y_level_short = -0.8500
        self.is_wavelanding = False
        self.waveland_time = 0.0

    def update(self, buttons, x_axis_value, y_axis_value):
        self.x_value = x_axis_value
        self.y_value = y_axis_value

        waveland_long = (buttons["left"].is_active or buttons["right"].is_active) and not buttons["down"].is_active
        waveland_short = (buttons["soft_left"].is_active or buttons["soft_right"].is_active) and not waveland_long

        if buttons["air_dodge"].just_activated:
            self.is_wavelanding = True
            self.waveland_time = time.perf_counter()

        if self.is_wavelanding and not buttons["down"].is_active:
            if time.perf_counter() - self.waveland_time < 0.025:
                if waveland_long:
                    self.x_value = normalize(x_axis_value) * self.x_level_long
                    self.y_value = self.y_level_long

                elif waveland_short:
                    self.x_value = normalize(x_axis_value) * self.x_level_short
                    self.y_value = self.y_level_short

                else:
                    self.y_value = -1.0

            else:
                self.is_wavelanding = False
