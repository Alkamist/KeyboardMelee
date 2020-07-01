class AngledSmasher(object):
    def __init__(self):
        self.c_y_value = 0.0

    def update(self, buttons, y_axis_value, c_y_axis_value):
        self.c_y_value = c_y_axis_value

        if (buttons["mod1"].is_active or buttons["mod2"].is_active) \
        and (buttons["c_left"].is_active or buttons["c_right"].is_active):
            if y_axis_value > 0.0:
                self.c_y_value = 0.7
            elif y_axis_value < 0.0:
                self.c_y_value = -0.7
