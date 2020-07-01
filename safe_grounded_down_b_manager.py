import time

from normalize import normalize


class SafeGroundedDownBManager(object):
    def __init__(self):
        self.x_value = 0.0
        self.y_value = 0.0
        self.x_level = 0.5875
        self.y_level = 0.6000
        self.is_doing_safe_b = False
        self.safe_b_time = 0.0

    def update(self, buttons, x_axis_value, y_axis_value):
        self.x_value = x_axis_value
        self.y_value = y_axis_value

        if buttons["b"].just_activated and (buttons["down"] or buttons["up"]):
            self.is_doing_safe_b = True
            self.safe_b_time = time.perf_counter()

        if self.is_doing_safe_b:
            if time.perf_counter() - self.safe_b_time < 0.025:
                self.x_value = normalize(x_axis_value) * self.x_level
                self.y_value = normalize(y_axis_value) * self.y_level
            else:
                self.is_doing_safe_b = False
