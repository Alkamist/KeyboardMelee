class State(object):
    def __init__(self):
        self.is_active = False
        self.was_active = False

    @property
    def just_activated(self):
        return self.is_active and not self.was_active

    @property
    def just_deactivated(self):
        return self.was_active and not self.is_active

    def update(self):
        self.was_active = self.is_active
