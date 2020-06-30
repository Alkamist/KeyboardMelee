import time

from state import State


class BackdashOutOfCrouchFixer(object):
    def __init__(self):
        self.x_value = 0.0
        self.left_state = State()
        self.right_state = State()
        self.down_state = State()
        self.backdash_time = 0.0
        self.delay_backdash = False

    def update(self, down, left, right, disable_if, x_axis_value):
        self.left_state.update()
        self.right_state.update()
        self.down_state.update()
        self.left_state.is_active = left
        self.right_state.is_active = right
        self.down_state.is_active = down

        self.x_value = x_axis_value

        if down and (self.left_state.just_activated or self.right_state.just_activated) and not disable_if:
            self.delay_backdash = True
            self.backdash_time = time.perf_counter()

        if self.down_state.just_deactivated:
            self.delay_backdash = False

        if self.delay_backdash:
            self.x_value = 0.0
            if time.perf_counter() - self.backdash_time >= 0.04:
                self.delay_backdash = False
