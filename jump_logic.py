import time


class JumpLogic(object):
    def __init__(self, buttons, outputs):
        self.buttons = buttons
        self.outputs = outputs
        self.is_full_hopping = False
        self.is_short_hopping = False
        self.short_hop_time = 0.0
        self.full_hop_time = 0.0
        self.short_hop_output = False
        self.full_hop_output = False

    def update(self):
        buttons = self.buttons

        start_short_hop = buttons["short_hop"].just_activated or (self.is_full_hopping and buttons["full_hop"].just_activated)

        if start_short_hop:
            self.short_hop_output = True
            self.is_short_hopping = True
            self.short_hop_time = time.perf_counter()

        if self.is_short_hopping and time.perf_counter() - self.short_hop_time >= 0.025:
            self.short_hop_output = False
            self.is_short_hopping = False

        start_full_hop = not self.is_full_hopping and buttons["full_hop"].just_activated

        if start_full_hop:
            self.is_full_hopping = True
            self.full_hop_output = True
            self.full_hop_time = time.perf_counter()

        if self.is_full_hopping and not buttons["full_hop"].is_active:
            if time.perf_counter() - self.full_hop_time >= 0.134:
                self.full_hop_output = False

            # Wait one extra frame so you can't miss a double jump by
            # pushing the full hop button on the same frame of release.
            if time.perf_counter() - self.full_hop_time >= 0.150:
                self.is_full_hopping = False

        self.outputs["y"] = self.short_hop_output
        self.outputs["x"] = self.full_hop_output
