from state import State


class LightShieldLogic(object):
    def __init__(self):
        self.shield_output = False
        self.light_shield_output = 0
        self.is_light_shielding = False
        self._light_shield_state = State()
        self._shield_state = State()

    def update(self, shield, light_shield):
        self._light_shield_state.is_active = light_shield
        self._shield_state.is_active = shield
        self._light_shield_state.update()
        self._shield_state.update()

        if self._shield_state.is_active and self._light_shield_state.just_activated:
            self.is_light_shielding = not self.is_light_shielding

        if self._shield_state.just_deactivated:
            self.is_light_shielding = False

        if self.is_light_shielding:
            self.shield_output = False
            self.light_shield_output = 43
        else:
            self.shield_output = shield
            self.light_shield_output = 0
