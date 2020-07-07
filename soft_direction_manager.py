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

        soft_is_pressed = (buttons["soft_left"].is_active or buttons["soft_right"].is_active)
        reset_on_soft_press = buttons["soft_left"].just_activated or buttons["soft_right"].just_activated
        reset_on_down_up = soft_is_pressed and (buttons["up"].just_activated or buttons["down"].just_activated)
        reset_on_release = soft_is_pressed and (buttons["soft_left"].just_deactivated or buttons["soft_right"].just_deactivated)
        reset_tilt = reset_on_soft_press or reset_on_down_up or reset_on_release

        if reset_tilt:
            self.tilt_time = time.perf_counter()

        suspend_tilt = (not buttons["b"].is_active) \
                   and (buttons["short_hop"].is_active or buttons["full_hop"].is_active) \
                   and (buttons["left"].is_active or buttons["right"].is_active)
        should_tilt = time.perf_counter() - self.tilt_time <= 0.100

        sideways = buttons["left"].is_active or buttons["right"].is_active or buttons["soft_left"].is_active or buttons["soft_right"].is_active
        diagonal = sideways and (buttons["down"].is_active or buttons["up"].is_active)

        if should_tilt and not suspend_tilt:
            if buttons["b"].is_active:
                self.x_value = normalize(x_axis_value) * 0.3000
                self.y_value = normalize(y_axis_value) * 0.6500

            else:
                if diagonal and not buttons["mod1"].is_active:
                    x_multiplier = 0.3000
                else:
                    x_multiplier = 0.6500

                self.x_value = normalize(x_axis_value) * x_multiplier
                self.y_value = normalize(y_axis_value) * 0.6500

        elif soft_is_pressed:
            self.y_value = normalize(y_axis_value) * 0.9500
