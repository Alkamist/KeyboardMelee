class State(object):
    def __init__(self):
        self.was_active = False
        self.just_activated = False
        self.just_deactivated = False

        self._pending_state = False
        self._state = False

    @property
    def is_active(self):
        return self._state

    @is_active.setter
    def is_active(self, state):
        self._pending_state = state

    def update(self):
        self.was_active = self._state
        self._state = self._pending_state
        self.just_activated = self.is_active and not self.was_active
        self.just_deactivated = self.was_active and not self.is_active
