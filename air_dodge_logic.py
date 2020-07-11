import time


class AirDodgeLogic(object):
    def __init__(self, buttons, outputs):
        self.buttons = buttons
        self.outputs = outputs
        self.x_level_long = 0.9375
        self.y_level_long = -0.3125
        self.x_level_short = 0.5000
        self.y_level_short = -0.8500
        self.is_wavelanding = False
        self.waveland_time = 0.0

    def update(self):
        buttons = self.buttons

        sideways = (buttons["left"].is_active or buttons["right"].is_active) and not buttons["down"].is_active

        waveland_short = sideways and buttons["tilt"].is_active
        waveland_long = sideways and not waveland_short

        if buttons["air_dodge"].just_activated:
            self.is_wavelanding = True
            self.waveland_time = time.perf_counter()

        if self.is_wavelanding and not buttons["down"].is_active:
            if time.perf_counter() - self.waveland_time < 0.051:
                if waveland_long:
                    self.outputs["ls_x"] = self.outputs["ls_x_raw"] * self.x_level_long
                    self.outputs["ls_y"] = self.y_level_long

                elif waveland_short:
                    self.outputs["ls_x"] = self.outputs["ls_x_raw"] * self.x_level_short
                    self.outputs["ls_y"] = self.y_level_short

                else:
                    self.outputs["ls_y"] = -1.0

            else:
                self.is_wavelanding = False
