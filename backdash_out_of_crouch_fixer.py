import time


class BackdashOutOfCrouchFixer(object):
    def __init__(self):
        self.x_value = 0.0
        self.backdash_time = 0.0
        self.delay_backdash = False

    def update(self, buttons, disable_if, x_axis_value):
        self.x_value = x_axis_value

        if buttons["down"].is_active and (buttons["left"].just_activated or buttons["right"].just_activated):
            self.delay_backdash = True
            self.backdash_time = time.perf_counter()

        if buttons["down"].just_deactivated or disable_if:
            self.delay_backdash = False

        if self.delay_backdash:
            self.x_value = 0.0
            if time.perf_counter() - self.backdash_time >= 0.1:
                self.delay_backdash = False
