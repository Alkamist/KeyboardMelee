class State(object):
    def __init__(self):
        self.is_active = False
        self.was_active = False
        self.just_activated = False
        self.just_deactivated = False
        self.pending_state = False

    def update(self):
        self.was_active = self.is_active
        self.is_active = self.pending_state
        self.just_activated = self.is_active and not self.was_active
        self.just_deactivated = self.was_active and not self.is_active
