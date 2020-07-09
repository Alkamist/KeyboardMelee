import time


class ATiltLogic(object):
    def __init__(self, buttons, outputs):
        self.buttons = buttons
        self.outputs = outputs
        self.tilt_time = 0.0
        self.neutral_time = 0.0
        self.delay_a_for = 0.0
        self.should_press_a = False
        self.a_output = False
        self.a_press_time = 0.0
        self.suppress_c_stick = False

    def update(self):
        buttons = self.buttons

        is_holding_tilt_mod = (buttons["soft_left"].is_active or buttons["soft_right"].is_active) and not buttons["disable_tilt"].is_active
        any_c_button = buttons["c_up"].just_activated or buttons["c_down"].just_activated \
                    or buttons["c_left"].just_activated or buttons["c_right"].just_activated
        should_do_tilt = is_holding_tilt_mod and any_c_button

        if should_do_tilt:
            self.tilt_time = time.perf_counter()
            self.suppress_c_stick = True
            if buttons["c_left"].is_active and (buttons["right"].is_active or buttons["soft_right"].is_active) \
            or buttons["c_right"].is_active and (buttons["left"].is_active or buttons["soft_left"].is_active):
                self.delay_a_for = 0.035
            else:
                self.should_press_a = True
                self.delay_a_for = 0.0

        if self.delay_a_for > 0.0 and time.perf_counter() - self.tilt_time >= self.delay_a_for:
            self.should_press_a = True
            self.delay_a_for = 0.0


        # Handle pressing a.
        hold_a_tilt = buttons["c_up"].is_active or buttons["c_down"].is_active \
                   or buttons["c_left"].is_active or buttons["c_right"].is_active

        if self.should_press_a:
            self.a_output = True
            self.a_press_time = time.perf_counter()
            self.should_press_a = False

        stop_a_press = self.a_output and (not hold_a_tilt) and time.perf_counter() - self.a_press_time >= 0.025

        if stop_a_press:
            self.a_output = False
            self.suppress_c_stick = False


        # Write the outputs.
        self.outputs["a"] = self.a_output or self.buttons["a"].is_active
        if self.suppress_c_stick:
            self.outputs["c_x"] = 0.0
            self.outputs["c_y"] = 0.0

        if time.perf_counter() - self.tilt_time <= 0.067:
            should_bias_x = (buttons["soft_left"].is_active or buttons["soft_right"].is_active) \
                        and not (buttons["c_left"].is_active or buttons["c_right"].is_active)
            x_bias = 0.35 * self.outputs["ls_x_raw"] if should_bias_x else 0.0
            self.outputs["ls_x"] = self.outputs["c_x_raw"] * 0.6000 + x_bias

            should_bias_y = (buttons["down"].is_active or buttons["up"].is_active) \
                        and (buttons["soft_left"].is_active or buttons["soft_right"].is_active) \
                        and not (buttons["c_down"].is_active or buttons["c_up"].is_active)
            y_bias = 0.5 * self.outputs["ls_y_raw"] if should_bias_y else 0.0
            self.outputs["ls_y"] = self.outputs["c_y_raw"] * 0.6000 + y_bias


        # Handle neutral a press.
        if self.buttons["a"].just_activated and not buttons["disable_tilt"].is_active:
            self.neutral_time = time.perf_counter()

        if time.perf_counter() - self.neutral_time < 0.025:
            self.outputs["ls_x"] = 0.0
            self.outputs["ls_y"] = 0.0
