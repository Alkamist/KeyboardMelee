import time

from normalize import normalize


class SoftDirectionManager(object):
    def __init__(self):
        self.x_value = 0.0
        self.y_value = 0.0
        self.release_linger_time = 0.0

    def update(self, buttons, x_axis_value, y_axis_value):
        self.x_value = x_axis_value
        self.y_value = y_axis_value

        if (buttons["soft_left"].just_deactivated or buttons["soft_right"].just_deactivated) \
        and (buttons["up"].is_active or buttons["down"].is_active):
            self.release_linger_time = time.perf_counter()

        tilt_should_linger = (time.perf_counter() - self.release_linger_time <= 0.100) and (buttons["up"].is_active or buttons["down"].is_active)
        suspend_tilt = (not buttons["b"].is_active) \
                   and (buttons["short_hop"].is_active or buttons["full_hop"].is_active) \
                   and (buttons["left"].is_active or buttons["right"].is_active)
        should_tilt = buttons["soft_left"].is_active or buttons["soft_right"].is_active or tilt_should_linger

        if should_tilt and not suspend_tilt:
            if buttons["b"].is_active:
                self.x_value = normalize(x_axis_value) * 0.3000
                self.y_value = normalize(y_axis_value) * 0.6500

            else:
                self.x_value = normalize(x_axis_value) * 0.6500
                self.y_value = normalize(y_axis_value) * 0.6500
