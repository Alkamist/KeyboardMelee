import time

from state import State
from normalize import normalize


class ShieldTiltManager(object):
    def __init__(self):
        self.x_value = 0.0
        self.y_value = 0.0
        self.shield_state = State()
        self.left_state = State()
        self.right_state = State()
        self.is_tilting_shield = False
        self.shield_tilt_time = 0.0
        self.y_tilt_level = 0.6000
        self.x_level = 0.6625
        self.y_level = 0.6625 # Shield drop value.

    def update(self, shield, air_dodge, left, right, down, mod1, x_axis_value, y_axis_value):
        self.shield_state.update()
        self.left_state.update()
        self.right_state.update()
        self.shield_state.is_active = shield
        self.left_state.is_active = left
        self.right_state.is_active = right

        self.x_value = x_axis_value
        self.y_value = y_axis_value

        tilt_temporarily = shield and (self.left_state.just_activated or self.right_state.just_activated)
        tilt_temporarily_on_release = shield and ((self.left_state.just_deactivated and right) \
                                               or (self.right_state.just_deactivated and left))
        tilt_shield_down = down and shield
        initiate_shield_tilt = self.shield_state.just_activated or tilt_temporarily or tilt_temporarily_on_release or tilt_shield_down

        if initiate_shield_tilt:
            self.is_tilting_shield = True
            self.shield_tilt_time = time.perf_counter()

        if self.is_tilting_shield and not air_dodge:
            if time.perf_counter() - self.shield_tilt_time < 0.100:
                self.x_value = normalize(x_axis_value) * self.x_level
                if mod1:
                    self.y_value = normalize(y_axis_value) * self.y_tilt_level
                else:
                    self.y_value = normalize(y_axis_value) * self.y_level
            else:
                self.is_tilting_shield = False
