from state import State


class ButtonAxis(object):
    def __init__(self):
        self.value = 0.0
        self.low_was_first = False
        self.low_state = State()
        self.high_state = State()

    def update(self, low, high):
        self.low_state.is_active = low
        self.high_state.is_active = high
        self.low_state.update()
        self.high_state.update()

        if self.low_state.just_activated or (self.low_state.is_active and not self.high_state.is_active):
            self.value = -1.0

        elif self.high_state.just_activated or (self.high_state.is_active and not self.low_state.is_active):
            self.value = 1.0

        elif not self.low_state.is_active and not self.high_state.is_active:
            self.value = 0.0
