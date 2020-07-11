import time


class TiltLogic(object):
    def __init__(self, buttons, outputs):
        self.buttons = buttons
        self.outputs = outputs
        self.minimum_axis_scale = 0.2875
        self.tilt_level = 0.6500
        self.tilt_time = 0.0

    def update(self):
        buttons = self.buttons

        reset_on_direction_press = buttons["up"].just_activated or buttons["down"].just_activated \
                                or buttons["left"].just_activated or buttons["right"].just_activated
        reset_on_direction_release = buttons["up"].just_deactivated or buttons["down"].just_deactivated \
                                  or buttons["left"].just_deactivated or buttons["right"].just_deactivated
        reset_tilt = reset_on_direction_press or reset_on_direction_release

        if buttons["tilt"].is_active and reset_tilt:
            self.tilt_time = time.perf_counter()

        if time.perf_counter() - self.tilt_time <= 0.117:
            self.outputs["ls_x"] = self.tilt_axis(self.outputs["ls_x"])
            self.outputs["ls_y"] = self.tilt_axis(self.outputs["ls_y"])

    def tilt_axis(self, axis_value):
        scaled_axis = axis_value * self.tilt_level
        if axis_value > 0.0:
            return max(scaled_axis, self.minimum_axis_scale)
        elif axis_value < 0.0:
            return min(scaled_axis, -self.minimum_axis_scale)
        else:
            return 0.0
