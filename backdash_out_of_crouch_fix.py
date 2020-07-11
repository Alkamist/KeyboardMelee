import time


class BackdashOutOfCrouchFix(object):
    def __init__(self, buttons, outputs):
        self.buttons = buttons
        self.outputs = outputs
        self.backdash_time = 0.0
        self.delay_backdash = False

    def update(self):
        buttons = self.buttons

        if buttons["down"].is_active and (buttons["left"].just_activated or buttons["right"].just_activated) \
        and not buttons["tilt"].is_active:
            self.delay_backdash = True
            self.backdash_time = time.perf_counter()

        disable_if = buttons["a"].is_active or buttons["b"].is_active or buttons["z"].is_active or buttons["air_dodge"].is_active \
                  or buttons["shield"].is_active or buttons["short_hop"].is_active or buttons["full_hop"].is_active

        if buttons["down"].just_deactivated or disable_if:
            self.delay_backdash = False

        if self.delay_backdash:
            self.outputs["ls_x"] = 0.0
            if time.perf_counter() - self.backdash_time >= 0.1:
                self.delay_backdash = False
