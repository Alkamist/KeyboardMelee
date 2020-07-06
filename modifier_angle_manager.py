import time

from normalize import normalize


class ModifierAngleManager(object):
    def __init__(self):
        self.x_value = 0.0
        self.y_value = 0.0
        self.mod1_x = 0.6625
        self.mod1_y = 0.2875
        self.mod2_x = 0.2875
        self.mod2_y = 0.9500
        self.b_time = 0.0

    def update(self, buttons, x_axis_value, y_axis_value):
        self.x_value = x_axis_value
        self.y_value = y_axis_value

        if buttons["b"].just_activated:
            self.b_time = time.perf_counter()

        if buttons["mod1"].is_active and time.perf_counter() - self.b_time > 0.025:
            self.x_value = normalize(x_axis_value) * self.mod1_x
            self.y_value = normalize(y_axis_value) * self.mod1_y

        elif buttons["mod2"].is_active and time.perf_counter() - self.b_time > 0.025:
            self.x_value = normalize(x_axis_value) * self.mod2_x
            self.y_value = normalize(y_axis_value) * self.mod2_y
