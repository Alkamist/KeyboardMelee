from state import State


class LightShieldLogic(object):
    def __init__(self, buttons, outputs):
        self.buttons = buttons
        self.outputs = outputs
        self.is_light_shielding = False

    def update(self):
        buttons = self.buttons

        if buttons["shield"].is_active and buttons["light_shield"].just_activated:
            self.is_light_shielding = not self.is_light_shielding

        if buttons["shield"].just_deactivated:
            self.is_light_shielding = False

        if self.is_light_shielding:
            self.outputs["l"] = False
            self.outputs["l_analog"] = 43
        else:
            self.outputs["l"] = buttons["shield"].is_active
            self.outputs["l_analog"] = 0
