from vjoy_device import VJoyDevice


class ButtonOutput(object):
    def __init__(self, vjoy_device, id, value):
        self.vjoy_device = vjoy_device
        self.value = value
        self.previous_value = value
        self.id = id

    def update(self):
        if self.value != self.previous_value:
            self.vjoy_device.set_button(self.id, self.value)

        self.previous_value = self.value


class AxisOutput(object):
    def __init__(self, vjoy_device, name, value):
        self.vjoy_device = vjoy_device
        self.value = value
        self.previous_value = value
        self.name = name
        self.axis_max_scale = 0.626

    def update(self):
        if self.value != self.previous_value:
            self.vjoy_device.set_axis(self.name, 0.5 * (self.axis_max_scale * self.value + 1.0))

        self.previous_value = self.value


class SliderOutput(object):
    def __init__(self, vjoy_device, name, value):
        self.vjoy_device = vjoy_device
        self.value = value
        self.previous_value = value
        self.name = name

    def update(self):
        if self.value != self.previous_value:
            zero_to_one_value = self.value / 255.0
            proper_value = 0.5 - 0.5 * zero_to_one_value
            self.vjoy_device.set_axis(self.name, proper_value)

        self.previous_value = self.value


class GameController(object):
    def __init__(self, device_id=1):
        self.vjoy_device = VJoyDevice(1)

        self.real_outputs = {
            "a" : ButtonOutput(self.vjoy_device, 1, False),
            "b" : ButtonOutput(self.vjoy_device, 2, False),
            "x" : ButtonOutput(self.vjoy_device, 3, False),
            "y" : ButtonOutput(self.vjoy_device, 4, False),
            "z" : ButtonOutput(self.vjoy_device, 5, False),
            "l" : ButtonOutput(self.vjoy_device, 6, False),
            "r" : ButtonOutput(self.vjoy_device, 7, False),
            "start" : ButtonOutput(self.vjoy_device, 8, False),
            "d_left" : ButtonOutput(self.vjoy_device, 9, False),
            "d_right" : ButtonOutput(self.vjoy_device, 10, False),
            "d_down" : ButtonOutput(self.vjoy_device, 11, False),
            "d_up" : ButtonOutput(self.vjoy_device, 12, False),
            "ls_x" : AxisOutput(self.vjoy_device, "x", 0.0),
            "ls_y" : AxisOutput(self.vjoy_device, "y", 0.0),
            "c_x" : AxisOutput(self.vjoy_device, "rx", 0.0),
            "c_y" : AxisOutput(self.vjoy_device, "ry", 0.0),
            "l_analog" : SliderOutput(self.vjoy_device, "rz", 0),
            #"r_analog" : 0.0,
        }

        self.send_outputs()

    def send_outputs(self, outputs=None):
        for output_name, output in self.real_outputs.items():
            if outputs is not None:
                output.value = outputs[output_name]
            output.update()
