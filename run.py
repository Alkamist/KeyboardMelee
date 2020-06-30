import time

from pynput import keyboard
from game_controller import GameController
from state import State
from button_axis import ButtonAxis
from jump_manager import JumpManager
from waveland_angle_manager import WavelandAngleManager


binds = {
    "up" : keyboard.KeyCode.from_char("w"),
    "down" : keyboard.KeyCode.from_char("s"),
    "right" : keyboard.KeyCode.from_char("d"),
    "left" : keyboard.KeyCode.from_char("a"),
    "x_mod" : keyboard.Key.shift_l,
    "y_mod" : keyboard.Key.alt_l,

    "c_up" : keyboard.KeyCode.from_char("p"),
    "c_down" : keyboard.KeyCode.from_char("."),
    "c_right" : keyboard.KeyCode.from_char("/"),
    "c_left" : keyboard.KeyCode.from_char(","),

    "d_up" : keyboard.KeyCode.from_char("g"),
    "d_down" : keyboard.KeyCode.from_char("b"),
    "d_right" : keyboard.KeyCode.from_char("h"),
    "d_left" : keyboard.KeyCode.from_char("v"),

    "short_hop" : keyboard.KeyCode.from_char("["),
    "full_hop" : keyboard.KeyCode.from_char("\\"),

    "a" : keyboard.KeyCode.from_char("'"),
    "b" : keyboard.KeyCode.from_char(";"),
    "z" : keyboard.KeyCode.from_char("]"),

    "shield" : keyboard.Key.space,
    "air_dodge" : keyboard.Key.alt_r,

    "start" : keyboard.KeyCode.from_char("5"),
}

buttons = {}
for name in binds:
    buttons[name] = State()


def on_key_press(key):
    for bind_name, key_value in binds.items():
        if key == key_value:
            buttons[bind_name].is_active = True

def on_key_release(key):
    for bind_name, key_value in binds.items():
        if key == key_value:
            buttons[bind_name].is_active = False

keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
keyboard_listener.start()


controller = GameController(1)

jump_manager = JumpManager()
waveland_angle_manager = WavelandAngleManager()
ls_x_raw = ButtonAxis()
ls_y_raw = ButtonAxis()
c_x_raw = ButtonAxis()
c_y_raw = ButtonAxis()


while True:
    ls_x_out = 0.0
    ls_y_out = 0.0

    ls_x_raw.update(buttons["left"].is_active, buttons["right"].is_active)
    ls_x_out = ls_x_raw.value

    ls_y_raw.update(buttons["down"].is_active, buttons["up"].is_active)
    ls_y_out = ls_y_raw.value

    c_x_raw.update(buttons["c_left"].is_active, buttons["c_right"].is_active)
    c_y_raw.update(buttons["c_down"].is_active, buttons["c_up"].is_active)

    jump_manager.update(
        short_hop=buttons["short_hop"].is_active,
        full_hop=buttons["full_hop"].is_active,
    )

    waveland_angle_manager.update(
        air_dodge=buttons["air_dodge"].is_active,
        left=buttons["left"].is_active,
        right=buttons["right"].is_active,
        down=buttons["down"].is_active,
        x_axis_value=ls_x_raw.value,
        y_axis_value=ls_y_raw.value,
    )
    if waveland_angle_manager.is_wavelanding:
        ls_x_out = waveland_angle_manager.x_value
        ls_y_out = waveland_angle_manager.y_value

    controller.a = buttons["a"].is_active
    controller.b = buttons["b"].is_active
    controller.x = jump_manager.full_hop_value
    controller.y = jump_manager.short_hop_value
    controller.z = buttons["z"].is_active
    controller.l = buttons["shield"].is_active
    controller.r = buttons["air_dodge"].is_active
    controller.start = buttons["start"].is_active
    controller.d_left = buttons["d_left"].is_active
    controller.d_right = buttons["d_right"].is_active
    controller.d_down = buttons["d_down"].is_active
    controller.d_up = buttons["d_up"].is_active
    controller.ls_x = ls_x_out
    controller.ls_y = ls_y_out
    controller.c_x = c_x_raw.value
    controller.c_y = c_y_raw.value
    #controller.l_analog = 0.0
    #controller.r_analog = 0.0

    controller.send_outputs()

    for state in buttons.values():
        state.update()

    time.sleep(0.001)
