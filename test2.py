import time

from pynput import keyboard#, mouse
from game_controller import GameController


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


keybinds = {
    "up" : keyboard.KeyCode.from_char("w"),
    "down" : keyboard.KeyCode.from_char("s"),
    "right" : keyboard.KeyCode.from_char("d"),
    "left" : keyboard.KeyCode.from_char("a"),
    "x_mod" : keyboard.Key.shift_l,
    "y_mod" : keyboard.Key.alt_l,

    "c_up" : keyboard.Key.up,
    "c_down" : keyboard.Key.down,
    "c_right" : keyboard.Key.right,
    "c_left" : keyboard.Key.left,

    "d_up" : keyboard.KeyCode.from_char("g"),
    "d_down" : keyboard.KeyCode.from_char("b"),
    "d_right" : keyboard.KeyCode.from_char("h"),
    "d_left" : keyboard.KeyCode.from_char("v"),

    "short_hop" : keyboard.KeyCode.from_vk(104),
    "full_hop" : keyboard.KeyCode.from_char("+"),

    "a" : keyboard.KeyCode.from_vk(96),
    "b" : keyboard.KeyCode.from_vk(100),
    "z" : keyboard.KeyCode.from_vk(105),

    "shield" : keyboard.Key.space,
    "air_dodge" : keyboard.KeyCode.from_vk(103),

    "start" : keyboard.Key.enter,
}

buttons = {}
for name in keybinds:
    buttons[name] = State()


#def on_mouse_move(x, y):
#    pass
#
#def on_mouse_click(x, y, button, pressed):
#    pass
#
#def on_mouse_scroll(x, y, dx, dy):
#    pass

def on_key_press(key):
    for bind_name, key_value in keybinds.items():
        if key == key_value:
            buttons[bind_name].is_active = True

def on_key_release(key):
    for bind_name, key_value in keybinds.items():
        if key == key_value:
            buttons[bind_name].is_active = False

keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
keyboard_listener.start()


controller = GameController(1)


ls_x_raw = ButtonAxis()
ls_y_raw = ButtonAxis()
c_x_raw = ButtonAxis()
c_y_raw = ButtonAxis()


while True:
    ls_x_raw.update(buttons["left"].is_active, buttons["right"].is_active)
    ls_y_raw.update(buttons["down"].is_active, buttons["up"].is_active)
    c_x_raw.update(buttons["c_left"].is_active, buttons["c_right"].is_active)
    c_y_raw.update(buttons["c_down"].is_active, buttons["c_up"].is_active)

    controller.a = buttons["a"].is_active
    controller.b = buttons["b"].is_active
    controller.x = buttons["full_hop"].is_active
    controller.y = buttons["short_hop"].is_active
    controller.z = buttons["z"].is_active
    controller.l = buttons["shield"].is_active
    controller.r = buttons["air_dodge"].is_active
    controller.start = buttons["start"].is_active
    controller.d_left = buttons["d_left"].is_active
    controller.d_right = buttons["d_right"].is_active
    controller.d_down = buttons["d_down"].is_active
    controller.d_up = buttons["d_up"].is_active
    controller.ls_x = ls_x_raw.value
    controller.ls_y = ls_y_raw.value
    controller.c_x = c_x_raw.value
    controller.c_y = c_y_raw.value
    #controller.l_analog = 0.0
    #controller.r_analog = 0.0

    controller.send_outputs()

    for state in buttons.values():
        state.update()

    time.sleep(0.001)
