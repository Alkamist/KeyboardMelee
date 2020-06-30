import time

import keyboard
from game_controller import GameController
from state import State
from button_axis import ButtonAxis
from jump_manager import JumpManager
from shield_tilt_manager import ShieldTiltManager
from waveland_angle_manager import WavelandAngleManager
from modifier_angle_manager import ModifierAngleManager
from safe_grounded_down_b_manager import SafeGroundedDownBManager
from backdash_out_of_crouch_fixer import BackdashOutOfCrouchFixer
from angled_smasher import AngledSmasher
from shield_manager import ShieldManager


key_binds = {
    "up" : "w",
    "down" : "s",
    "right" : "d",
    "left" : "a",
    "mod1" : "caps lock",
    "mod2" : "alt",

    "c_up" : "p",
    "c_down" : "right windows",
    "c_right" : "/",
    "c_left" : "l",

    "d_up" : "1",
    "d_down" : "2",
    "d_right" : "3",
    "d_left" : "4",

    "short_hop" : "[",
    "full_hop" : "\\",

    "a" : "'",
    "b" : ";",
    "z" : "]",

    "shield" : "space",
    "light_shield" : "-",
    "air_dodge" : "right alt",

    "start" : "5",
}
binds_reversed = dict((v, k) for k, v in key_binds.items())

buttons = {}
for name in key_binds:
    buttons[name] = State()

base_keys = {
    "!" : "1",
    "@" : "2",
    "#" : "3",
    "$" : "4",
    "%" : "5",
    "^" : "6",
    "&" : "7",
    "*" : "8",
    "(" : "9",
    ")" : "0",
    "_" : "-",
    "+" : "=",
    "{" : "[",
    "}" : "]",
    "|" : "\\",
    ":" : ";",
    "\"" : "'",
    "<" : ",",
    ">" : ".",
    "?" : "/",
    "~" : "`",
}

def get_base_key(key_name):
    if key_name in base_keys:
        return base_keys[key_name]
    else:
        if len(key_name) == 1:
            return key_name.lower()
        else:
            return key_name

def on_press_key(key):
    key_name = get_base_key(key.name)
    if key_name in binds_reversed:
        bind_name = binds_reversed[key_name]
        buttons[bind_name].is_active = True

def on_release_key(key):
    key_name = get_base_key(key.name)
    if key_name in binds_reversed:
        bind_name = binds_reversed[key_name]
        buttons[bind_name].is_active = False

for bind_name, bind_value in key_binds.items():
    keyboard.on_press_key(keyboard.parse_hotkey(bind_value), on_press_key, True)
    keyboard.on_release_key(keyboard.parse_hotkey(bind_value), on_release_key, True)


controller = GameController(1)

jump_manager = JumpManager()
shield_tilt_manager = ShieldTiltManager()
waveland_angle_manager = WavelandAngleManager()
modifier_angle_manager = ModifierAngleManager()
safe_grounded_down_b_manager = SafeGroundedDownBManager()
backdash_out_of_crouch_fixer = BackdashOutOfCrouchFixer()
angled_smasher = AngledSmasher()
shield_manager = ShieldManager()
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
    c_y_out = c_y_raw.value

    jump_manager.update(
        short_hop=buttons["short_hop"].is_active,
        full_hop=buttons["full_hop"].is_active,
    )

    shield_manager.update(
        light_shield=buttons["light_shield"].is_active,
        shield=buttons["shield"].is_active,
    )

    angled_smasher.update(
        mod1=buttons["mod1"].is_active,
        mod2=buttons["mod2"].is_active,
        c_left=buttons["c_left"].is_active,
        c_right=buttons["c_right"].is_active,
        y_axis_value=ls_y_out,
        c_y_axis_value=c_y_out,
    )
    c_y_out = angled_smasher.c_y_value

    backdash_out_of_crouch_fixer.update(
        down=buttons["down"].is_active,
        left=buttons["left"].is_active,
        right=buttons["right"].is_active,
        disable_if=buttons["a"].is_active or buttons["b"].is_active or buttons["z"].is_active or buttons["air_dodge"].is_active \
                   or buttons["shield"].is_active or buttons["short_hop"].is_active or buttons["full_hop"].is_active,
        x_axis_value=ls_x_out,
    )
    ls_x_out = backdash_out_of_crouch_fixer.x_value

    safe_grounded_down_b_manager.update(
        b=buttons["b"].is_active,
        down=buttons["down"].is_active,
        up=buttons["up"].is_active,
        x_axis_value=ls_x_out,
        y_axis_value=ls_y_out,
    )
    ls_x_out = safe_grounded_down_b_manager.x_value
    ls_y_out = safe_grounded_down_b_manager.y_value

    modifier_angle_manager.update(
        mod1=buttons["mod1"].is_active,
        mod2=buttons["mod2"].is_active,
        x_axis_value=ls_x_out,
        y_axis_value=ls_y_out,
    )
    ls_x_out = modifier_angle_manager.x_value
    ls_y_out = modifier_angle_manager.y_value

    waveland_angle_manager.update(
        air_dodge=buttons["air_dodge"].is_active,
        left=buttons["left"].is_active,
        right=buttons["right"].is_active,
        down=buttons["down"].is_active,
        x_axis_value=ls_x_out,
        y_axis_value=ls_y_out,
    )
    ls_x_out = waveland_angle_manager.x_value
    ls_y_out = waveland_angle_manager.y_value

    shield_tilt_manager.update(
        shield=buttons["shield"].is_active,
        air_dodge=buttons["air_dodge"].is_active,
        left=buttons["left"].is_active,
        right=buttons["right"].is_active,
        down=buttons["down"].is_active,
        mod1=buttons["mod1"].is_active,
        x_axis_value=ls_x_out,
        y_axis_value=ls_y_out,
    )
    ls_x_out = shield_tilt_manager.x_value
    ls_y_out = shield_tilt_manager.y_value

    controller.a = buttons["a"].is_active
    controller.b = buttons["b"].is_active
    controller.x = jump_manager.full_hop_value
    controller.y = jump_manager.short_hop_value
    controller.z = buttons["z"].is_active
    controller.l = shield_manager.shield_value
    controller.r = buttons["air_dodge"].is_active
    controller.start = buttons["start"].is_active
    controller.d_left = buttons["d_left"].is_active
    controller.d_right = buttons["d_right"].is_active
    controller.d_down = buttons["d_down"].is_active
    controller.d_up = buttons["d_up"].is_active
    controller.ls_x = ls_x_out
    controller.ls_y = ls_y_out
    controller.c_x = c_x_raw.value
    controller.c_y = c_y_out
    controller.l_analog = shield_manager.light_shield_value

    controller.send_outputs()

    for button in buttons.values():
        button.update()

    time.sleep(0.001)
