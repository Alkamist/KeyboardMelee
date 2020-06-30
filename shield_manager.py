from state import State


class ShieldManager(object):
    def __init__(self):
        self.shield_value = False
        self.light_shield_value = 0
        self.is_light_shielding = False
        self.shield_state = State()
        self.light_shield_state = State()

    def update(self, light_shield, shield):
        self.shield_state.update()
        self.light_shield_state.update()
        self.shield_state.is_active = shield
        self.light_shield_state.is_active = light_shield

        self.shield_value = shield

        if shield and self.light_shield_state.just_activated:
            self.is_light_shielding = not self.is_light_shielding

        if self.shield_state.just_deactivated:
            self.is_light_shielding = False

        if self.is_light_shielding:
            self.shield_value = False
            self.light_shield_value = 43
        else:
            self.light_shield_value = 0
