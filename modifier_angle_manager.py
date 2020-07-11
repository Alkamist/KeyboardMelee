import time


class ModifierAngleManager(object):
    def __init__(self, buttons, outputs):
        self.buttons = buttons
        self.outputs = outputs
        self.y_mod_x = 0.9500
        self.y_mod_y = 0.2875
        self.x_mod_x = 0.2875
        self.x_mod_y = 0.9500
        self.b_time = 0.0

    def update(self):
        buttons = self.buttons

        if buttons["b"].just_activated:
            self.b_time = time.perf_counter()

        if buttons["y_mod"].is_active and time.perf_counter() - self.b_time > 0.025:
            self.outputs["ls_x"] = self.outputs["ls_x_raw"] * self.y_mod_x
            self.outputs["ls_y"] = self.outputs["ls_y_raw"] * self.y_mod_y

        elif buttons["x_mod"].is_active and time.perf_counter() - self.b_time > 0.025:
            self.outputs["ls_x"] = self.outputs["ls_x_raw"] * self.x_mod_x
            self.outputs["ls_y"] = self.outputs["ls_y_raw"] * self.x_mod_y
