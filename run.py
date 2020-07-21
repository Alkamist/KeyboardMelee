import time

from button_manager import ButtonManager
from game_controller import GameController
from state import State
from button_axis import ButtonAxis
from jump_logic import JumpLogic
from light_shield_logic import LightShieldLogic
from shield_tilt_logic import ShieldTiltLogic
from air_dodge_logic import AirDodgeLogic
from backdash_out_of_crouch_fix import BackdashOutOfCrouchFix
from a_stick import AStick
from b_stick import BStick
from tilt_stick import TiltStick
from modifier_angle_logic import ModifierAngleLogic


use_short_hop = True

key_binds = {
    "up" : "w",
    "down" : "s",
    "right" : "d",
    "left" : "a",
    "tilt" : "caps lock",
    "x_mod" : "alt",
    "y_mod" : "space",

    "invert_x" : "right shift",

    "c_up" : "p",
    "c_down" : "'",
    "c_right" : "/",
    "c_left" : "l",

    "charge_smash" : "tab",

    "d_up" : "g",
    "d_down" : "b",
    "d_right" : "n",
    "d_left" : "v",

    "short_hop" : ("[", "-"),
    "full_hop" : "\\",

    "a" : "right windows",
    "z" : "=",

    "b_up" : "backspace",
    "b_neutral_down" : "right alt",
    "b_side" : "enter",

    "shield" : "]",
    "light_shield" : "shift",
    "air_dodge" : ";",

    "start" : "5",

    "toggle_script" : "8",
}

outputs = {
    "ls_x" : 0.0,
    "ls_x_raw" : 0.0,
    "ls_y" : 0.0,
    "ls_y_raw" : 0.0,
    "c_x" : 0.0,
    "c_x_raw" : 0.0,
    "c_y" : 0.0,
    "c_y_raw" : 0.0,
    "l_analog" : 0,
    "a" : False,
    "b" : False,
    "x" : False,
    "y" : False,
    "z" : False,
    "l" : False,
    "r" : False,
    "start" : False,
    "d_left" : False,
    "d_right" : False,
    "d_down" : False,
    "d_up" : False,
}


controller = GameController(1)

button_manager = ButtonManager(key_binds)
buttons = button_manager.buttons

jump_logic = JumpLogic()
light_shield_logic = LightShieldLogic()
shield_tilt_logic = ShieldTiltLogic()
air_dodge_logic = AirDodgeLogic()
backdash_out_of_crouch_fix = BackdashOutOfCrouchFix()
a_stick = AStick()
b_stick = BStick()
tilt_stick = TiltStick()
modifier_angle_logic = ModifierAngleLogic()


ls_x_raw = ButtonAxis()
ls_y_raw = ButtonAxis()
c_x_raw = ButtonAxis()
c_y_raw = ButtonAxis()


script_is_disabled = False
last_direction_is_right = True

while True:
    button_manager.update()

    outputs["a"] = buttons["a"].is_active
    outputs["b"] = False
    outputs["x"] = buttons["full_hop"].is_active
    outputs["y"] = buttons["short_hop"].is_active
    outputs["z"] = buttons["z"].is_active
    outputs["l"] = buttons["shield"].is_active
    outputs["r"] = buttons["air_dodge"].is_active
    outputs["start"] = buttons["start"].is_active
    outputs["d_left"] = buttons["d_left"].is_active
    outputs["d_right"]= buttons["d_right"].is_active
    outputs["d_down"] = buttons["d_down"].is_active
    outputs["d_up"] = buttons["d_up"].is_active

    ls_x_raw.update(buttons["left"].is_active, buttons["right"].is_active)
    outputs["ls_x_raw"] = ls_x_raw.value
    outputs["ls_x"] = ls_x_raw.value

    ls_y_raw.update(buttons["down"].is_active, buttons["up"].is_active)
    outputs["ls_y_raw"] = ls_y_raw.value
    outputs["ls_y"] = ls_y_raw.value

    c_x_raw.update(buttons["c_left"].is_active, buttons["c_right"].is_active)
    outputs["c_x_raw"] = c_x_raw.value
    outputs["c_x"] = c_x_raw.value

    c_y_raw.update(buttons["c_down"].is_active, buttons["c_up"].is_active)
    outputs["c_y_raw"] = c_y_raw.value
    outputs["c_y"] = c_y_raw.value

    if buttons["invert_x"].is_active:
        outputs["ls_x_raw"] = -outputs["ls_x_raw"]
        outputs["ls_x"] = -outputs["ls_x"]

    if use_short_hop:
        jump_logic.update(
            short_hop=buttons["short_hop"].is_active,
            full_hop=buttons["full_hop"].is_active,
        )
        outputs["y"] = jump_logic.short_hop_output
        outputs["x"] = jump_logic.full_hop_output

    light_shield_logic.update(
        shield=buttons["shield"].is_active,
        light_shield=buttons["light_shield"].is_active,
    )
    outputs["l"] = light_shield_logic.shield_output
    outputs["l_analog"] = light_shield_logic.light_shield_output

    backdash_out_of_crouch_fix.update(
        down=buttons["down"].is_active,
        left=buttons["left"].is_active,
        right=buttons["right"].is_active,
        tilt=buttons["tilt"].is_active,
        ls_x=outputs["ls_x"],
    )
    if not (buttons["full_hop"].is_active or buttons["short_hop"].is_active or buttons["z"].is_active or buttons["shield"].is_active \
            or buttons["air_dodge"].is_active or buttons["a"].is_active or buttons["b_up"].is_active or buttons["b_neutral_down"].is_active \
            or buttons["b_side"].is_active):
        outputs["ls_x"] = backdash_out_of_crouch_fix.x_axis_output

    modifier_angle_logic.update(
        x_mod=buttons["x_mod"].is_active,
        y_mod=buttons["y_mod"].is_active,
        ls_x_raw=ls_x_raw.value,
        ls_y_raw=ls_y_raw.value,
        ls_x=outputs["ls_x"],
        ls_y=outputs["ls_y"],
    )
    outputs["ls_x"] = modifier_angle_logic.x_axis_output
    outputs["ls_y"] = modifier_angle_logic.y_axis_output

    shield_tilt_logic.update(
        shield=buttons["shield"].is_active,
        ls_x=outputs["ls_x"],
        ls_y=outputs["ls_y"],
    )
    outputs["ls_x"] = shield_tilt_logic.x_axis_output
    outputs["ls_y"] = shield_tilt_logic.y_axis_output

    if not buttons["shield"].is_active:
        a_stick_condition = buttons["tilt"].is_active
        a_stick.update(
            a_neutral=buttons["a"].is_active,
            a_left=buttons["c_left"].is_active and a_stick_condition,
            a_right=buttons["c_right"].is_active and a_stick_condition,
            a_down=buttons["c_down"].is_active and a_stick_condition,
            a_up=buttons["c_up"].is_active and a_stick_condition,
            ls_x_raw=ls_x_raw.value,
            ls_y_raw=ls_y_raw.value,
            ls_x=outputs["ls_x"],
            ls_y=outputs["ls_y"],
        )
        outputs["a"] = a_stick.a_state.is_active
        outputs["ls_x"] = a_stick.x_axis_output
        outputs["ls_y"] = a_stick.y_axis_output
        if a_stick_condition:
            outputs["c_x"] = 0.0
            outputs["c_y"] = 0.0

    tilt_stick.update(
        tilt_modifier=buttons["tilt"].is_active,
        hold_tilt=buttons["tilt"].is_active and buttons["shield"].is_active,
        ls_x=outputs["ls_x"],
        ls_y=outputs["ls_y"],
    )
    outputs["ls_x"] = tilt_stick.x_axis_output
    outputs["ls_y"] = tilt_stick.y_axis_output

    if ls_x_raw.value > 0.0:
        last_direction_is_right = True
    elif ls_x_raw.value < 0.0:
        last_direction_is_right = False

    b_stick.update(
        b_neutral=buttons["b_neutral_down"].is_active and not buttons["down"].is_active,
        b_left=buttons["b_side"].is_active and not last_direction_is_right,
        b_right=buttons["b_side"].is_active and last_direction_is_right,
        b_down=buttons["b_neutral_down"].is_active and buttons["down"].is_active,
        b_up=buttons["b_up"].is_active,
        ls_x_raw=ls_x_raw.value,
        ls_x=outputs["ls_x"],
        ls_y=outputs["ls_y"],
    )
    outputs["b"] = b_stick.b_state.is_active
    outputs["ls_x"] = b_stick.x_axis_output
    outputs["ls_y"] = b_stick.y_axis_output

    air_dodge_logic.update(
        air_dodge=buttons["air_dodge"].is_active,
        tilt=buttons["tilt"].is_active,
        left=buttons["left"].is_active,
        right=buttons["right"].is_active,
        down=buttons["down"].is_active,
        up=buttons["up"].is_active,
        ls_x_raw=ls_x_raw.value,
        ls_x=outputs["ls_x"],
        ls_y=outputs["ls_y"],
    )
    outputs["ls_x"] = air_dodge_logic.x_axis_output
    outputs["ls_y"] = air_dodge_logic.y_axis_output

    if buttons["charge_smash"].is_active:
        outputs["a"] = outputs["a"] or buttons["c_left"].is_active or buttons["c_right"].is_active \
                                    or buttons["c_down"].is_active or buttons["c_up"].is_active

    # Allow for angled smashes when holding down or up on the left stick.
    c_diagonal = (buttons["c_left"].is_active or buttons["c_right"].is_active) and (buttons["up"].is_active or buttons["down"].is_active)
    if c_diagonal and not buttons["tilt"].is_active:
        outputs["c_y"] = ls_y_raw.value * 0.4

    # Allow the script to be toggled on and off with a key.
    if buttons["toggle_script"].just_activated:
        if script_is_disabled:
            button_manager.bind_keys()
        else:
            button_manager.unbind_keys()
        script_is_disabled = not script_is_disabled

    controller.send_outputs(outputs)

    time.sleep(0.0001)
