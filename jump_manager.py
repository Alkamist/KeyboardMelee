import time

from state import State


class JumpManager(object):
    def __init__(self):
        self.short_hop_state = State()
        self.full_hop_state = State()
        self.short_hop_value = False
        self.full_hop_value = False
        self.is_full_hopping = False
        self.is_short_hopping = False
        self.short_hop_time = 0.0
        self.full_hop_time = 0.0

    def update(self, short_hop, full_hop):
        self.short_hop_state.update()
        self.full_hop_state.update()
        self.short_hop_state.is_active = short_hop
        self.full_hop_state.is_active = full_hop

        if self.short_hop_state.just_activated or (self.is_full_hopping and self.full_hop_state.just_activated):
            self.short_hop_value = True
            self.is_short_hopping = True
            self.short_hop_time = time.perf_counter()

        if not self.is_full_hopping and self.full_hop_state.just_activated:
            self.is_full_hopping = True
            self.full_hop_value = True
            self.full_hop_time = time.perf_counter()

        if self.is_short_hopping:
            if time.perf_counter() - self.short_hop_time >= 0.025:
                self.short_hop_value = False
                self.is_short_hopping = False

        if self.is_full_hopping and not self.full_hop_state.is_active:
            if time.perf_counter() - self.full_hop_time >= 0.134:
                self.full_hop_value = False

            # Wait one extra frame so you can't miss a double jump by
            # pushing the full hop button on the same frame of release.
            if time.perf_counter() - self.full_hop_time >= 0.150:
                self.is_full_hopping = False
