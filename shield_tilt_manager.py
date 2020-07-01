import time

from normalize import normalize


class ShieldTiltManager(object):
    def __init__(self):
        self.x_value = 0.0
        self.y_value = 0.0
        self.is_tilting_shield = False
        self.shield_tilt_time = 0.0
        self.y_tilt_level = 0.6000
        self.x_level = 0.6625
        self.y_level = 0.6625 # Shield drop value.

    def update(self, buttons, x_axis_value, y_axis_value):
        self.x_value = x_axis_value
        self.y_value = y_axis_value

        tilt_temporarily = buttons["shield"].is_active and (buttons["left"].just_activated or buttons["right"].just_activated)
        tilt_temporarily_on_release = buttons["shield"].is_active and ((buttons["left"].just_deactivated and buttons["right"].is_active) \
                                                                    or (buttons["right"].just_deactivated and buttons["left"].is_active))
        tilt_shield_down = buttons["down"].is_active and buttons["shield"].is_active
        initiate_shield_tilt = buttons["shield"].just_activated or tilt_temporarily or tilt_temporarily_on_release or tilt_shield_down

        if initiate_shield_tilt:
            self.is_tilting_shield = True
            self.shield_tilt_time = time.perf_counter()

        if self.is_tilting_shield and not buttons["air_dodge"].is_active:
            if time.perf_counter() - self.shield_tilt_time < 0.100:
                self.x_value = normalize(x_axis_value) * self.x_level
                if buttons["mod1"].is_active:
                    self.y_value = normalize(y_axis_value) * self.y_tilt_level
                else:
                    self.y_value = normalize(y_axis_value) * self.y_level
            else:
                self.is_tilting_shield = False
