import time

from state import State


class JumpLogic(object):
    def __init__(self):
        self.short_hop_output = False
        self.full_hop_output = False

        self._is_full_hopping = False
        self._is_short_hopping = False
        self._short_hop_time = 0.0
        self._full_hop_time = 0.0
        self._short_hop_input = State()
        self._full_hop_input = State()

    def update(self, short_hop, full_hop):
        self._short_hop_input.is_active = short_hop
        self._full_hop_input.is_active = full_hop
        self._short_hop_input.update()
        self._full_hop_input.update()


        start_short_hop = self._short_hop_input.just_activated or (self._is_full_hopping and self._full_hop_input.just_activated)

        if start_short_hop:
            self.short_hop_output = True
            self._is_short_hopping = True
            self._short_hop_time = time.perf_counter()

        if self._is_short_hopping and time.perf_counter() - self._short_hop_time >= 0.025:
            self.short_hop_output = False
            self._is_short_hopping = False

        start_full_hop = not self._is_full_hopping and self._full_hop_input.just_activated

        if start_full_hop:
            self._is_full_hopping = True
            self.full_hop_output = True
            self._full_hop_time = time.perf_counter()

        if self._is_full_hopping and not self._full_hop_input.is_active:
            if time.perf_counter() - self._full_hop_time >= 0.134:
                self.full_hop_output = False

            # Wait one extra frame so you can't miss a double jump by
            # pushing the full hop button on the same frame of release.
            if time.perf_counter() - self._full_hop_time >= 0.150:
                self._is_full_hopping = False
