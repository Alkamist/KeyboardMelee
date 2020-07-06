import time

from normalize import normalize


class SoftDirectionManager(object):
    def __init__(self):
        self.x_value = 0.0
        self.y_value = 0.0
        self.tilt_time = 0.0

    def update(self, buttons, x_axis_value, y_axis_value):
        self.x_value = x_axis_value
        self.y_value = y_axis_value

        is_soft_direction = buttons["soft_left"].is_active or buttons["soft_right"].is_active

        if is_soft_direction:
            if buttons["up"].just_activated or buttons["down"].just_activated \
            or buttons["soft_left"].just_activated or buttons["soft_right"].just_activated \
            or (buttons["soft_left"].just_deactivated and buttons["soft_right"].is_active) \
            or (buttons["soft_right"].just_deactivated and buttons["soft_left"].is_active):
                self.tilt_time = time.perf_counter()

            if time.perf_counter() - self.tilt_time < 0.100:
                self.x_value = normalize(x_axis_value) * 0.6500
                self.y_value = normalize(y_axis_value) * 0.6500
