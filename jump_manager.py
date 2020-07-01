import time


class JumpManager(object):
    def __init__(self):
        self.short_hop_value = False
        self.full_hop_value = False
        self.is_full_hopping = False
        self.is_short_hopping = False
        self.short_hop_time = 0.0
        self.full_hop_time = 0.0

    def update(self, buttons):
        if buttons["short_hop"].just_activated or (self.is_full_hopping and buttons["full_hop"].just_activated):
            self.short_hop_value = True
            self.is_short_hopping = True
            self.short_hop_time = time.perf_counter()

        if not self.is_full_hopping and buttons["full_hop"].just_activated:
            self.is_full_hopping = True
            self.full_hop_value = True
            self.full_hop_time = time.perf_counter()

        if self.is_short_hopping:
            if time.perf_counter() - self.short_hop_time >= 0.025:
                self.short_hop_value = False
                self.is_short_hopping = False

        if self.is_full_hopping and not buttons["full_hop"].is_active:
            if time.perf_counter() - self.full_hop_time >= 0.134:
                self.full_hop_value = False

            # Wait one extra frame so you can't miss a double jump by
            # pushing the full hop button on the same frame of release.
            if time.perf_counter() - self.full_hop_time >= 0.150:
                self.is_full_hopping = False
