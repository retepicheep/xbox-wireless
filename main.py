from pprint import pprint
import atexit
import hid
import time
import logging


def calculate_axis_value(i, deadzone) -> int:
    abs_max = (65535/2)
    adjusted_i = i - abs_max

    if abs(adjusted_i) < deadzone:
        return 0.0
    else:
        if adjusted_i < 0:
            return (adjusted_i + deadzone) / (abs_max - deadzone)
        else:
            return (adjusted_i - deadzone) / (abs_max - deadzone)


class Axis(object):
    def __init__(self, x, y, deadzone=4000):
        self.x = calculate_axis_value(x, deadzone)
        self.y = calculate_axis_value(y, deadzone)

    def __str__(self) -> str:
        return f"(x={self.x}, y={self.y})"


class DPad(object):
    def __init__(self, dpad_state):
        self.state = dpad_state
        self.up = dpad_state in [1, 2, 8]
        self.right = dpad_state in [2, 3, 4]
        self.down = dpad_state in [4, 5, 6]
        self.left = dpad_state in [6, 7, 8]

    def __str__(self) -> str:
        return f"(up={self.up}, right={self.right}, down={self.down}, {self.left})"


class XboxControllerState(object):
    # Max - 65535
    # Min - 0
    def __init__(self, data):
        self.left_stick = Axis(
            x=data[1] + (data[2] * 256), 
            y=data[3] + (data[4] * 256),
        )

        self.right_stick = Axis(
            x=data[5] + (data[6] * 256), 
            y=data[7] + (data[8] * 256),
        )
    
        self.left_trigger = data[9] + (data[10] * 256)

        self.right_trigger = data[11] + (data[12] * 256)

        self.dpad = DPad(data[13])

    def __str__(self) -> str:
        return f"XboxControllerState(lj={self.left_stick}, rj={self.right_stick}, lt={self.left_trigger}, rt={self.right_trigger}, dpad={self.dpad})"

class XboxController(object):
    _state = None
    _observers = []

    def __init__(self, vendor_id=1118, product_id=2835) -> None:
        self.controller = hid.device()
        self.controller.open(vendor_id, product_id)
        self.controller.set_nonblocking(True)
        atexit.register(self._close)

    def _close(self) -> None:
        if self.controller:
            logging.debug("Closing device")
            self.controller.close()
            delattr(self, "controller")

    def attach(self, observer) -> None:
        logging.debug("Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer) -> None:
        logging.debug("Detach an observer.")
        self._observers.remove(observer)

    def notify_x_button(self) -> None:
        for observer in self._observers:
            observer_method = getattr(observer, "x_button", None)
            if callable(observer_method):
                observer_method()
    
    def monitor(self) -> None:
        while True:
            report = self.controller.read(64)
            if report:
                print(XboxControllerState(report))
                # print(report)
                # print([report[i] for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]])
                print([report[i] for i in [0, 13, 14, 15]])
                #print(report[11:13])
                time.sleep(.5)
                # print(report[13], report[14])
                # if report[14] == 8:
                #     self.notify_x_button()

def print_xbox_device_info() -> None:
    for device in hid.enumerate():
        if device["product_string"] == "Xbox Wireless Controller":
            print("#" * 100)
            print(f"# 0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")
            print("#" * 100)
            pprint(device)


class GameObject(object):
    def __init__(self, shooting_noise="Pew"):
        self.shooting_noise = shooting_noise

    def x_button(self) -> None:
        print(self.shooting_noise)


# gamepad = hid.device()
# gamepad.open(0x045e, 0x0b13)
# gamepad.set_nonblocking(True)

# while True:
#     report = gamepad.read(64)
#     if report:
#         print(report)

# print_xbox_device_info()

x = XboxController()
a = GameObject()
x.attach(a)
b = GameObject("Bang")
x.attach(b)

x.monitor()
