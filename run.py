import time

from button_manager import ButtonManager
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
from spammer import Spammer
from soft_direction_manager import SoftDirectionManager


use_short_hop = True

key_binds = {
    "up" : "w",
    "down" : "s",
    "right" : "d",
    "left" : "a",
    "soft_left" : "q",
    "soft_right" : "e",
    "mod1" : "space",
    "mod2" : "alt",

    "c_up" : "p",
    "c_down" : "[",
    "c_right" : "/",
    "c_left" : "l",

    "d_up" : "1",
    "d_down" : "2",
    "d_right" : "3",
    "d_left" : "4",

    "short_hop" : "]",
    "full_hop" : "enter",

    "a" : "'",
    "b" : ";",
    "z" : "\\",

    "shield" : "caps lock",
    "light_shield" : "-",
    "air_dodge" : "right alt",

    "start" : "5",
}


controller = GameController(1)

button_manager = ButtonManager(key_binds)
buttons = button_manager.buttons

jump_manager = JumpManager()
shield_tilt_manager = ShieldTiltManager()
waveland_angle_manager = WavelandAngleManager()
modifier_angle_manager = ModifierAngleManager()
safe_grounded_down_b_manager = SafeGroundedDownBManager()
backdash_out_of_crouch_fixer = BackdashOutOfCrouchFixer()
angled_smasher = AngledSmasher()
shield_manager = ShieldManager()
soft_direction_manager = SoftDirectionManager()
b_spammer = Spammer()
ls_x_raw = ButtonAxis()
ls_y_raw = ButtonAxis()
c_x_raw = ButtonAxis()
c_y_raw = ButtonAxis()


while True:
    ls_x_out = 0.0
    ls_y_out = 0.0

    ls_x_raw.update(buttons["left"].is_active or buttons["soft_left"].is_active, buttons["right"].is_active or buttons["soft_right"].is_active)
    ls_x_out = ls_x_raw.value

    ls_y_raw.update(buttons["down"].is_active, buttons["up"].is_active)
    ls_y_out = ls_y_raw.value

    c_x_raw.update(buttons["c_left"].is_active, buttons["c_right"].is_active)
    c_y_raw.update(buttons["c_down"].is_active, buttons["c_up"].is_active)
    c_y_out = c_y_raw.value

    if use_short_hop:
        jump_manager.update(buttons=buttons)

    shield_manager.update(buttons=buttons)

    angled_smasher.update(
        buttons=buttons,
        y_axis_value=ls_y_out,
        c_y_axis_value=c_y_out,
    )
    c_y_out = angled_smasher.c_y_value

    backdash_out_of_crouch_fixer.update(
        buttons=buttons,
        disable_if=buttons["a"].is_active or buttons["b"].is_active or buttons["z"].is_active or buttons["air_dodge"].is_active \
                   or buttons["shield"].is_active or buttons["short_hop"].is_active or buttons["full_hop"].is_active,
        x_axis_value=ls_x_out,
    )
    ls_x_out = backdash_out_of_crouch_fixer.x_value

    safe_grounded_down_b_manager.update(
        buttons=buttons,
        x_axis_value=ls_x_out,
        y_axis_value=ls_y_out,
    )
    ls_x_out = safe_grounded_down_b_manager.x_value
    ls_y_out = safe_grounded_down_b_manager.y_value

    modifier_angle_manager.update(
        buttons=buttons,
        x_axis_value=ls_x_out,
        y_axis_value=ls_y_out,
    )
    ls_x_out = modifier_angle_manager.x_value
    ls_y_out = modifier_angle_manager.y_value

    soft_direction_manager.update(
        buttons=buttons,
        x_axis_value=ls_x_out,
        y_axis_value=ls_y_out,
    )
    ls_x_out = soft_direction_manager.x_value
    ls_y_out = soft_direction_manager.y_value

    waveland_angle_manager.update(
        buttons=buttons,
        x_axis_value=ls_x_out,
        y_axis_value=ls_y_out,
    )
    ls_x_out = waveland_angle_manager.x_value
    ls_y_out = waveland_angle_manager.y_value

    shield_tilt_manager.update(
        buttons=buttons,
        x_axis_value=ls_x_out,
        y_axis_value=ls_y_out,
    )
    ls_x_out = shield_tilt_manager.x_value
    ls_y_out = shield_tilt_manager.y_value

    b_spammer.update(
        start_spamming=buttons["a"].just_activated and buttons["b"].is_active,
        stop_spamming=buttons["a"].just_deactivated or buttons["b"].just_deactivated,
    )

    controller.a = buttons["a"].is_active
    controller.b = buttons["b"].is_active if not b_spammer.is_spamming else b_spammer.output_state.is_active
    controller.x = jump_manager.full_hop_value if use_short_hop else buttons["full_hop"].is_active
    controller.y = jump_manager.short_hop_value if use_short_hop else buttons["short_hop"].is_active
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
