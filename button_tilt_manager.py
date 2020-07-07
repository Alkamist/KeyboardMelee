import time

from normalize import normalize
from button_tilter import ButtonTilter


class ButtonTiltManager(object):
    def __init__(self, buttons):
        self.buttons = buttons
        self.x_value = 0.0
        self.y_value = 0.0
        self.c_x_value = 0.0
        self.c_y_value = 0.0
        self.a_value = False
        self.b_value = False
        self.a_tilter = ButtonTilter(self.buttons["mod1"])
        self.b_tilter = ButtonTilter(self.buttons["b"])
        self.neutral_time = 0.0

    def update(self, x_axis_value, y_axis_value, c_x_axis_value, c_y_axis_value):
        self.x_value = x_axis_value
        self.y_value = y_axis_value
        self.c_x_value = c_x_axis_value
        self.c_y_value = c_y_axis_value

        self.b_tilter.update(
            buttons=self.buttons,
            x_axis_value=self.x_value,
            y_axis_value=self.y_value,
            c_x_axis_value=self.c_x_value,
            c_y_axis_value=self.c_y_value,
        )
        self.x_value = self.b_tilter.x_value
        self.y_value = self.b_tilter.y_value
        self.c_x_value = self.b_tilter.c_x_value
        self.c_y_value = self.b_tilter.c_y_value
        self.b_value = self.b_tilter.button_value

        self.a_tilter.update(
            buttons=self.buttons,
            x_axis_value=self.x_value,
            y_axis_value=self.y_value,
            c_x_axis_value=self.c_x_value,
            c_y_axis_value=self.c_y_value,
        )
        bias_vertically = self.a_tilter.button_value and (self.buttons["up"].is_active or self.buttons["down"].is_active)
        tilt_bias = normalize(self.y_value) * 0.5000 if bias_vertically else 0.0

        self.x_value = self.a_tilter.x_value
        self.y_value = self.a_tilter.y_value + tilt_bias
        self.c_x_value = self.a_tilter.c_x_value
        self.c_y_value = self.a_tilter.c_y_value
        self.a_value = self.a_tilter.button_value or (self.buttons["a"].is_active and not self.buttons["b"].is_active)

        if self.buttons["a"].just_activated:
            self.neutral_time = time.perf_counter()

        if time.perf_counter() - self.neutral_time < 0.025:
            self.x_value = 0.0
            self.y_value = 0.0
