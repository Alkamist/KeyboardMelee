import time

from normalize import normalize


class ButtonTilter(object):
    def __init__(self, tilt_button):
        self.x_value = 0.0
        self.y_value = 0.0
        self.c_x_value = 0.0
        self.c_y_value = 0.0
        self.button_value = False
        self.tilt_button = tilt_button
        self.tilt_time = 0.0

    def update(self, buttons, x_axis_value, y_axis_value, c_x_axis_value, c_y_axis_value):
        self.x_value = x_axis_value
        self.y_value = y_axis_value
        self.c_x_value = c_x_axis_value
        self.c_y_value = c_y_axis_value

        if buttons["c_up"].just_activated or buttons["c_down"].just_activated \
        or buttons["c_left"].just_activated or buttons["c_right"].just_activated \
        or buttons["a"].just_activated:
            self.tilt_time = time.perf_counter()

        if self.tilt_button.is_active and time.perf_counter() - self.tilt_time <= 0.025:
            self.button_value = True
            self.x_value = normalize(c_x_axis_value) * 0.6000
            self.y_value = normalize(c_y_axis_value) * 0.6000
            self.c_x_value = 0.0
            self.c_y_value = 0.0

        else:
            self.button_value = False
