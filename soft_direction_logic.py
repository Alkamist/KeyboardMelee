import time


class SoftDirectionLogic(object):
    def __init__(self, buttons, outputs):
        self.buttons = buttons
        self.outputs = outputs
        self.tilt_time = 0.0

    def update(self):
        buttons = self.buttons

        soft_is_pressed = (buttons["soft_left"].is_active or buttons["soft_right"].is_active)
        reset_on_soft_press = buttons["soft_left"].just_activated or buttons["soft_right"].just_activated
        reset_on_release = soft_is_pressed and (buttons["soft_left"].just_deactivated or buttons["soft_right"].just_deactivated)
        reset_on_release_to_up = buttons["up"].is_active and (buttons["soft_left"].just_deactivated or buttons["soft_right"].just_deactivated)
        reset_tilt = reset_on_soft_press or reset_on_release or reset_on_release_to_up

        if reset_tilt:
            self.tilt_time = time.perf_counter()

        suspend_tilt_for_ledge_dash = (buttons["short_hop"].is_active or buttons["full_hop"].is_active) \
                                  and (buttons["left"].is_active or buttons["right"].is_active)
        suspend_tilt_for_down = soft_is_pressed and buttons["down"].is_active
        suspend_tilt = suspend_tilt_for_ledge_dash or suspend_tilt_for_down
        should_tilt = time.perf_counter() - self.tilt_time <= 0.100

        if should_tilt and not suspend_tilt:
            self.outputs["ls_x"] = self.outputs["ls_x_raw"] * 0.6500
            self.outputs["ls_y"] = self.outputs["ls_y_raw"] * 0.6500

        if soft_is_pressed:
            if buttons["down"].is_active:
                self.outputs["ls_y"] = self.outputs["ls_y_raw"] * 0.9500
            else:
                self.outputs["ls_y"] = self.outputs["ls_y_raw"] * 0.6500
