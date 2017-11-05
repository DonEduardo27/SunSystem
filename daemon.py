#!/usr/bin/python3

import avango.daemon
import os


def init_blue_spacemouse():
    _string = get_event_string(1, "3Dconnexion SpaceNavigator") # search for spacemouse

    if len(_string) > 0: # spacemouse was found
        _string = _string.split()[0]

        _spacemouse = avango.daemon.HIDInput()
        _spacemouse.station = avango.daemon.Station('gua-device-spacemouse') # create a station to propagate the input events
        _spacemouse.device = _string
        _spacemouse.timeout = '14' # better !
        _spacemouse.norm_abs = 'True'

        # map incoming spacemouse events to station values
        _spacemouse.values[0] = "EV_REL::REL_X"   # trans X
        _spacemouse.values[1] = "EV_REL::REL_Z"   # trans Y
        _spacemouse.values[2] = "EV_REL::REL_Y"   # trans Z
        _spacemouse.values[3] = "EV_REL::REL_RX"  # rotate X
        _spacemouse.values[4] = "EV_REL::REL_RZ"  # rotate Y
        _spacemouse.values[5] = "EV_REL::REL_RY"  # rotate Z

        # buttons
        _spacemouse.buttons[0] = "EV_KEY::BTN_0" # left button
        _spacemouse.buttons[1] = "EV_KEY::BTN_1" # right button

        device_list.append(_spacemouse)
        print("Blue SpaceMouse started at:", _string)

        return


    print("Blue SpaceMouse NOT found!")
    

def init_keyboard():

    keyboard_name = os.popen("ls /dev/input/by-id | grep \"-event-kbd\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()

    keyboard_name = keyboard_name.split()

    for i, name in enumerate(keyboard_name):

        keyboard = avango.daemon.HIDInput()
        keyboard.station = avango.daemon.Station('gua-device-keyboard' + str(i))
        keyboard.device = "/dev/input/by-id/" + name


        keyboard.buttons[0] = "EV_KEY::KEY_W"
        keyboard.buttons[1] = "EV_KEY::KEY_A"
        keyboard.buttons[2] = "EV_KEY::KEY_S"
        keyboard.buttons[3] = "EV_KEY::KEY_D"
        keyboard.buttons[4] = "EV_KEY::KEY_LEFT"
        keyboard.buttons[5] = "EV_KEY::KEY_RIGHT"
        keyboard.buttons[6] = "EV_KEY::KEY_UP"
        keyboard.buttons[7] = "EV_KEY::KEY_DOWN"
        keyboard.buttons[8] = "EV_KEY::KEY_Q"
        keyboard.buttons[9] = "EV_KEY::KEY_E"
        keyboard.buttons[10] = "EV_KEY::KEY_PAGEUP"
        keyboard.buttons[11] = "EV_KEY::KEY_PAGEDOWN"
        keyboard.buttons[12] = "EV_KEY::KEY_KPPLUS"
        keyboard.buttons[13] = "EV_KEY::KEY_KPMINUS"
        

        device_list.append(keyboard)
        print("Keyboard " + str(i) + " started at:", keyboard_name)


## Gets the event string of a given input device.
def get_event_string(STRING_NUM, DEVICE_NAME):

    # file containing all devices with additional information
    _device_file = os.popen("cat /proc/bus/input/devices").read()
    _device_file = _device_file.split("\n")
    
    DEVICE_NAME = '\"' + DEVICE_NAME + '\"'
    
    # lines in the file matching the device name
    _indices = []

    for _i, _line in enumerate(_device_file):
        if DEVICE_NAME in _line:
            _indices.append(_i)

    # if no device was found or the number is too high, return an empty string
    if len(_indices) == 0 or STRING_NUM > len(_indices):
        return ""

    # else captue the event number X of one specific device and return /dev/input/eventX
    else:
        _event_string_start_index = _device_file[_indices[STRING_NUM-1]+4].find("event")
                
        return "/dev/input/" + _device_file[_indices[STRING_NUM-1]+4][_event_string_start_index:].split(" ")[0]



device_list = []

init_blue_spacemouse()
init_keyboard()

avango.daemon.run(device_list)
