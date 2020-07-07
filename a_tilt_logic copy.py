import time


class ATiltLogic(object):
    def __init__(self, buttons, outputs):
        self.buttons = buttons
        self.outputs = outputs
        self.tilt_time = 0.0
        self.neutral_time = 0.0
        self.should_delay_a_press = False
        self.should_press_a = False
        self.a_output = False
        self.a_press_time = 0.0

    def update(self):
        buttons = self.buttons

        is_holding_tilt_mod = buttons["mod1"].is_active
        any_c_button = buttons["c_up"].just_activated or buttons["c_down"].just_activated \
                    or buttons["c_left"].just_activated or buttons["c_right"].just_activated
        should_do_tilt = is_holding_tilt_mod and any_c_button

        if should_do_tilt:
            self.tilt_time = time.perf_counter()
            self.should_delay_a_press = buttons["c_left"].is_active or buttons["c_right"].is_active
            if not self.should_delay_a_press:
                self.should_press_a = True

        if self.should_delay_a_press and time.perf_counter() - self.tilt_time >= 0.017:
            self.should_press_a = True
            self.should_delay_a_press = False


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


        # Write the outputs.
        self.outputs["a"] = self.a_output or self.buttons["a"].is_active
        if self.a_output or self.should_delay_a_press:
            self.outputs["c_x"] = 0.0
            self.outputs["c_y"] = 0.0
        if time.perf_counter() - self.tilt_time <= 0.045:
            self.outputs["ls_x"] = self.outputs["c_x_raw"] * 0.6000
            self.outputs["ls_y"] = self.outputs["c_y_raw"] * 0.6000


        # Handle neutral a press.
        if self.buttons["a"].just_activated:
            self.neutral_time = time.perf_counter()

        if time.perf_counter() - self.neutral_time < 0.025:
            self.outputs["ls_x"] = 0.0
            self.outputs["ls_y"] = 0.0
