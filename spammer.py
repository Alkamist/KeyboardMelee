import time

from state import State


class Spammer(object):
    def __init__(self):
        self.output_state = State()
        self.is_spamming = False
        self.spam_time = 0.0
        self.interval = 0.01666

    def update(self, start_spamming, stop_spamming):
        self.output_state.update()

        if start_spamming:
            self.is_spamming = True
            self.output_state.is_active = True
            self.spam_time = time.perf_counter()

        if stop_spamming:
            self.is_spamming = False
            self.output_state.is_active = False

        if self.is_spamming:
            if time.perf_counter() - self.spam_time >= self.interval:
                self.output_state.is_active = not self.output_state.is_active
                self.spam_time = time.perf_counter()
