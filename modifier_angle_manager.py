def normalize(value):
    if value > 0.0:
        return 1.0
    elif value < 0.0:
        return -1.0
    else:
        return 0.0


class ModifierAngleManager(object):
    def __init__(self):
        self.x_value = 0.0
        self.y_value = 0.0
        self.mod1_x = 0.6625
        self.mod1_y = 0.2875
        self.mod2_x = 0.3500
        self.mod2_y = 0.7375

    def update(self, buttons, x_axis_value, y_axis_value):
        self.x_value = x_axis_value
        self.y_value = y_axis_value

        if buttons["mod1"].is_active and not buttons["b"].is_active:
            self.x_value = normalize(x_axis_value) * self.mod1_x
            self.y_value = normalize(y_axis_value) * self.mod1_y
        elif buttons["mod2"].is_active:
            self.x_value = normalize(x_axis_value) * self.mod2_x
            self.y_value = normalize(y_axis_value) * self.mod2_y
