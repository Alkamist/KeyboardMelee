import time

from button_manager import ButtonManager
from game_controller import GameController
from state import State
from button_axis import ButtonAxis
from jump_logic import JumpLogic
from light_shield_logic import LightShieldLogic
from shield_tilt_logic import ShieldTiltLogic
from air_dodge_logic import AirDodgeLogic
from safe_grounded_down_b_logic import SafeGroundedDownBLogic
from backdash_out_of_crouch_fix import BackdashOutOfCrouchFix
from soft_direction_logic import SoftDirectionLogic
from a_tilt_logic import ATiltLogic
from modifier_angle_manager import ModifierAngleManager


use_short_hop = True

key_binds = {
    "up" : ("w", "enter"),
    "down" : "s",
    "right" : "d",
    "left" : "a",
    "soft_left" : "q",
    "soft_right" : "e",
    "mod1" : "space",
    "mod2" : "alt",

    "disable_tilt" : "tab",

    "c_up" : "p",
    "c_down" : "/",
    "c_right" : "'",
    "c_left" : "l",

    "d_up" : "g",
    "d_down" : "b",
    "d_right" : "n",
    "d_left" : "v",

    "short_hop" : "[",
    "full_hop" : "\\",

    "a" : "right windows",
    "b" : ";",
    "z" : "]",

    "shield" : "caps lock",
    "light_shield" : "-",
    "air_dodge" : "right alt",

    "start" : "5",
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

jump_logic = JumpLogic(buttons, outputs)
light_shield_logic = LightShieldLogic(buttons, outputs)
safe_grounded_down_b_logic = SafeGroundedDownBLogic(buttons, outputs)
shield_tilt_logic = ShieldTiltLogic(buttons, outputs)
air_dodge_logic = AirDodgeLogic(buttons, outputs)
backdash_out_of_crouch_fix = BackdashOutOfCrouchFix(buttons, outputs)
soft_direction_logic = SoftDirectionLogic(buttons, outputs)
a_tilt_logic = ATiltLogic(buttons, outputs)
modifier_angle_manager = ModifierAngleManager(buttons, outputs)


ls_x_raw = ButtonAxis()
ls_y_raw = ButtonAxis()
c_x_raw = ButtonAxis()
c_y_raw = ButtonAxis()


while True:
    button_manager.update()

    outputs["a"] = buttons["a"].is_active
    outputs["b"] = buttons["b"].is_active
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

    ls_x_raw.update(buttons["left"].is_active or buttons["soft_left"].is_active, buttons["right"].is_active or buttons["soft_right"].is_active)
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

    if use_short_hop:
        jump_logic.update()

    light_shield_logic.update()
    backdash_out_of_crouch_fix.update()
    safe_grounded_down_b_logic.update()
    modifier_angle_manager.update()
    shield_tilt_logic.update()
    soft_direction_logic.update()
    air_dodge_logic.update()
    a_tilt_logic.update()

    # Allow for angled smashes when doing diagonal c inputs.
    c_diagonal = (buttons["c_left"].is_active or buttons["c_right"].is_active) and (buttons["c_up"].is_active or buttons["c_down"].is_active)
    if c_diagonal:
        outputs["c_y"] = outputs["c_y"] * 0.5

    controller.send_outputs(outputs)

    time.sleep(0.001)
