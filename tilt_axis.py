import time

from state import State


def sign(value):
    if value >= 0.0:
        return 1.0
    else:
        return -1.0


class TiltAxis(object):
    def __init__(self, tilt_level=0.65, minimum_active_value=0.2875):
        self.value = 0.0
        self.tilt_level = tilt_level
        self.minimum_active_value = minimum_active_value
        self.is_tilting = False

        self._tilt_time = 0.0
        self._input_value = 0.0
        self._input_previous_value = 0.0
        self._external_reset_state = State()

    def update(self, input_value, external_reset_state=False, external_reset_requirement=True):
        self._input_previous_value = self._input_value
        self._input_value = input_value

        self._external_reset_state.is_active = external_reset_state
        self._external_reset_state.update()

        input_value_is_active = abs(self._input_value) >= self.minimum_active_value
        input_previous_value_is_active = abs(self._input_previous_value) >= self.minimum_active_value
        reset_tilt_on_activation = input_value_is_active and not input_previous_value_is_active
        reset_tilt_on_center_cross = input_value_is_active and input_previous_value_is_active \
                                 and sign(self._input_value) != sign(self._input_previous_value)
        reset_tilt = external_reset_requirement and (reset_tilt_on_activation or reset_tilt_on_center_cross or self._external_reset_state.just_activated)

        if reset_tilt:
            self.is_tilting = True
            self._tilt_time = time.perf_counter()

        if time.perf_counter() - self._tilt_time <= 0.117:
            if self._input_value > 0.0:
                self.value = min(self.tilt_level, self._input_value)
            elif self._input_value < 0.0:
                self.value = max(-self.tilt_level, self._input_value)
            else:
                self.value = 0.0
        else:
            self.value = self._input_value
            self.is_tilting = False
