import time


class SafeGroundedDownBLogic(object):
    def __init__(self, buttons, outputs):
        self.buttons = buttons
        self.outputs = outputs
        self.x_level = 0.5875
        self.y_level = 0.6000
        self.is_doing_safe_b = False
        self.safe_b_time = 0.0

    def update(self):
        buttons = self.buttons

        if buttons["b"].just_activated and (buttons["down"].is_active or buttons["up"].is_active):
            self.is_doing_safe_b = True
            self.safe_b_time = time.perf_counter()

        if self.is_doing_safe_b:
            if time.perf_counter() - self.safe_b_time < 0.025:
                self.outputs["ls_x"] = self.outputs["ls_x_raw"] * self.x_level
                self.outputs["ls_y"] = self.outputs["ls_y_raw"] * self.y_level
            else:
                self.is_doing_safe_b = False
