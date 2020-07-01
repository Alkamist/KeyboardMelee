from state import State


class ShieldManager(object):
    def __init__(self):
        self.shield_value = False
        self.light_shield_value = 0
        self.is_light_shielding = False

    def update(self, buttons):
        self.shield_value = buttons["shield"].is_active

        if buttons["light_shield"].is_active and buttons["light_shield"].just_activated:
            self.is_light_shielding = not self.is_light_shielding

        if buttons["shield"].just_deactivated:
            self.is_light_shielding = False

        if self.is_light_shielding:
            self.shield_value = False
            self.light_shield_value = 43
        else:
            self.light_shield_value = 0
