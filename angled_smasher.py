class AngledSmasher(object):
    def __init__(self):
        self.c_y_value = 0.0

    def update(self, mod1, mod2, c_left, c_right, y_axis_value, c_y_axis_value):
        self.c_y_value = c_y_axis_value

        if (mod1 or mod2) and (c_left or c_right):
            if y_axis_value > 0.0:
                self.c_y_value = 0.7
            elif y_axis_value < 0.0:
                self.c_y_value = -0.7
