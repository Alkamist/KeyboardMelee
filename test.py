import time

from vjoy_device import VJoyDevice
from key import Key


vjoy_device = VJoyDevice(1)

buttons = {
    "a" : Key("num 0"),
    "b" : Key("num 7"),
    "y" : Key("l"),
    "z" : Key("num 9"),
    "r" : Key("space"),
    "start" : Key("enter"),
    "up" : Key("w"),
    "down" : Key("s"),
    "left" : Key("a"),
    "right" : Key("d"),
    "c_up" : Key("up arrow"),
    "c_down" : Key("down arrow"),
    "c_left" : Key("left arrow"),
    "c_right" : Key("right arrow"),
}


class ButtonOutput(object):
    def __init__(self, id, value):
        self.value = value
        self.previous_value = value
        self.id = id

    def update(self):
        if self.value != self.previous_value:
            vjoy_device.set_button(self.id, self.value)

        self.previous_value = self.value

class AxisOutput(object):
    def __init__(self, name, value):
        self.value = value
        self.previous_value = value
        self.name = name

    def update(self):
        if self.value != self.previous_value:
            vjoy_device.set_axis(self.name, 0.5 * (self.value + 1.0))

        self.previous_value = self.value

outputs = {
    "a" : ButtonOutput(1, False),
    "b" : ButtonOutput(2, False),
    "x" : ButtonOutput(3, False),
    "y" : ButtonOutput(4, False),
    "z" : ButtonOutput(5, False),
    "l" : ButtonOutput(6, False),
    "r" : ButtonOutput(7, False),
    "start" : ButtonOutput(8, False),
    #"d_left" : ButtonOutput(9, False),
    #"d_right" : ButtonOutput(10, False),
    #"d_down" : ButtonOutput(11, False),
    #"d_up" : ButtonOutput(12, False),
    #"l_analog" : 0.0,
    #"r_analog" : 0.0,
    "ls_x" : AxisOutput("x", 0.0),
    "ls_y" : AxisOutput("y", 0.0),
    "c_x" : AxisOutput("rx", 0.0),
    "c_y" : AxisOutput("ry", 0.0),
}


class State(object):
    def __init__(self):
        self.is_active = False
        self.was_active = False

    @property
    def just_activated(self):
        return self.is_active and not self.was_active

    @property
    def just_deactivated(self):
        return self.was_active and not self.is_active

    def update(self):
        self.was_active = self.is_active

class ButtonAxis(object):
    def __init__(self):
        self.value = 0.0
        self.low_was_first = False
        self.low_state = State()
        self.high_state = State()

    def update(self, low, high):
        self.low_state.update()
        self.high_state.update()
        self.low_state.is_active = low
        self.high_state.is_active = high

        if self.low_state.just_activated or (self.low_state.is_active and not self.high_state.is_active):
            self.value = -1.0

        elif self.high_state.just_activated or (self.high_state.is_active and not self.low_state.is_active):
            self.value = 1.0

        elif not self.low_state.is_active and not self.high_state.is_active:
            self.value = 0.0


def send_outputs(a, b, x, y, z, l, r, start, ls_x, ls_y, c_x, c_y):
    outputs["a"].value = a
    outputs["b"].value = b
    outputs["x"].value = x
    outputs["y"].value = y
    outputs["z"].value = z
    outputs["l"].value = l
    outputs["r"].value = r
    outputs["start"].value = start
    outputs["ls_x"].value = ls_x
    outputs["ls_y"].value = ls_y
    outputs["c_x"].value = c_x
    outputs["c_y"].value = c_y

    for output in outputs.values():
        output.update()


ls_x_raw = ButtonAxis()
ls_y_raw = ButtonAxis()
c_x_raw = ButtonAxis()
c_y_raw = ButtonAxis()

while True:
    for button in buttons.values():
        button.update()

    ls_x_raw.update(buttons["left"].is_pressed, buttons["right"].is_pressed)
    ls_y_raw.update(buttons["down"].is_pressed, buttons["up"].is_pressed)
    c_x_raw.update(buttons["c_left"].is_pressed, buttons["c_right"].is_pressed)
    c_y_raw.update(buttons["c_down"].is_pressed, buttons["c_up"].is_pressed)

    send_outputs(
        a=buttons["a"].is_pressed,
        b=buttons["b"].is_pressed,
        x=False,
        y=buttons["y"].is_pressed,
        z=buttons["z"].is_pressed,
        l=False,
        r=buttons["r"].is_pressed,
        start=buttons["start"].is_pressed,
        ls_x=ls_x_raw.value,
        ls_y=ls_y_raw.value,
        c_x=c_x_raw.value,
        c_y=c_y_raw.value,
    )
