import keyboard

from state import State


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


class ButtonManager(object):
    def __init__(self, key_binds):
        self.key_binds = key_binds

        self.buttons = {}
        for name in self.key_binds:
            self.buttons[name] = State()

        self.key_binds_reversed = {}
        for bind_name, bind_value in self.key_binds.items():
            if isinstance(bind_value, tuple):
                for i in range(len(bind_value)):
                    self.key_binds_reversed[bind_value[i]] = bind_name
            else:
                self.key_binds_reversed[bind_value] = bind_name

        self.key_is_pressed = {}
        for key_name in self.key_binds_reversed:
            self.key_is_pressed[key_name] = False

        def on_press_key(key):
            key_name = get_base_key(key.name)
            if key_name in self.key_binds_reversed:
                self.key_is_pressed[key_name] = True
                bind_name = self.key_binds_reversed[key_name]
                self.buttons[bind_name].is_active = True

        def on_release_key(key):
            key_name = get_base_key(key.name)
            if key_name in self.key_binds_reversed:
                bind_name = self.key_binds_reversed[key_name]

                another_same_bind_is_pressed = False
                if isinstance(self.key_binds[bind_name], tuple):
                    for physical_key in self.key_binds[bind_name]:
                        if key_name != physical_key and keyboard.is_pressed(physical_key):
                            another_same_bind_is_pressed = True

                if not another_same_bind_is_pressed:
                    self.buttons[bind_name].is_active = False

        for bind_name, bind_value in self.key_binds.items():
            if isinstance(bind_value, tuple):
                for i in range(len(bind_value)):
                    keyboard.on_press_key(keyboard.parse_hotkey(bind_value[i]), on_press_key, True)
                    keyboard.on_release_key(keyboard.parse_hotkey(bind_value[i]), on_release_key, True)
            else:
                keyboard.on_press_key(keyboard.parse_hotkey(bind_value), on_press_key, True)
                keyboard.on_release_key(keyboard.parse_hotkey(bind_value), on_release_key, True)
