import time


class ModifierAngleManager(object):
    def __init__(self, buttons, outputs):
        self.buttons = buttons
        self.outputs = outputs
        self.mod1_x = 0.9500
        self.mod1_y = 0.2875
        self.mod2_x = 0.2875
        self.mod2_y = 0.9500
        self.b_time = 0.0

    def update(self):
        buttons = self.buttons

        if buttons["b"].just_activated:
            self.b_time = time.perf_counter()

        if buttons["mod1"].is_active and time.perf_counter() - self.b_time > 0.025:
            self.outputs["ls_x"] = self.outputs["ls_x_raw"] * self.mod1_x
            self.outputs["ls_y"] = self.outputs["ls_y_raw"] * self.mod1_y

        elif buttons["mod2"].is_active and time.perf_counter() - self.b_time > 0.025:
            self.outputs["ls_x"] = self.outputs["ls_x_raw"] * self.mod2_x
            self.outputs["ls_y"] = self.outputs["ls_y_raw"] * self.mod2_y
