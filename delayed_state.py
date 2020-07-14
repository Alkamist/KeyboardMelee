import time

from state import State


class DelayedState(object):
    def __init__(self, delay=0.0, minimum_hold_time=0.025):
        self.delay = delay
        self.minimum_hold_time = minimum_hold_time

        self._input_state = State()
        self._output_state = State()
        self._queue_time = 0.0
        self._press_time = 0.0
        self._should_activate = False

    @property
    def is_active(self):
        return self._output_state.is_active

    @is_active.setter
    def is_active(self, state):
        self._input_state.is_active = state
        if self._input_state.just_activated:
            self._should_activate = True
            self._queue_time = time.perf_counter()

    @property
    def was_active(self):
        return self._output_state.was_active

    @property
    def just_activated(self):
        return self._output_state.just_activated

    @property
    def just_deactivated(self):
        return self._output_state.just_deactivated

    def update(self):
        self._input_state.update()
        self._output_state.update()

        if self._should_activate and time.perf_counter() - self._queue_time >= self.delay:
            self._press_time = time.perf_counter()
            self._output_state.is_active = True
            self._should_activate = False

        stop_press = self._output_state.is_active and (not self._input_state.is_active) \
                 and time.perf_counter() - self._press_time >= self.minimum_hold_time

        if stop_press:
            self._output_state.is_active = False
