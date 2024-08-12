from pprint import pprint
import atexit
import hid
import time
import logging


def calculate_axis_value(i, deadzone) -> int:
    abs_max = 65535 / 2
    adjusted_i = i - abs_max

    if abs(adjusted_i) < deadzone:
        return 0.0
    else:
        if adjusted_i < 0:
            return (adjusted_i + deadzone) / (abs_max - deadzone)
        else:
            return (adjusted_i - deadzone) / (abs_max - deadzone)


def find_hid_devices(vendor_id=1118, product_id=2835) -> list:
    hid_devices = []
    for h in hid.enumerate(vendor_id, product_id):
        hid_devices.append(h)
    return hid_devices
    # return hid.enumerate(vendor_id, product_id)


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
        return f"(up={self.up}, right={self.right}, down={self.down}, left={self.left})"


class Button(object):
    def __init__(self, buttons):
        self.buttons = buttons
        self.a = True if buttons & 1 else False
        self.b = True if buttons & 2 else False
        self.x = True if buttons & 8 else False
        self.y = True if buttons & 16 else False
        self.lb = True if buttons & 64 else False
        self.rb = True if buttons & 128 else False

    def pressed_buttons(self):
        button_list = []
        if self.x:
            button_list.append("x_button")
        if self.y:
            button_list.append("y_button")

        return button_list

    def get_state(self, button):
        if button == "x_button":
            return self.x
        elif button == "y_button":
            return self.y

    def __str__(self) -> str:
        return f"(a={self.a}, b={self.b}, x={self.x}, y={self.y}, lb={self.lb}, rb={self.rb})"


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
        self.buttons = Button(data[14])

    def __str__(self) -> str:
        return f"XboxControllerState(lj={self.left_stick}, rj={self.right_stick}, lt={self.left_trigger}, rt={self.right_trigger}, dpad={self.dpad}, buttons={self.buttons})"


class XboxController(object):
    _state = None
    _observers = []

    def __init__(
        self,
        vendor_id=1118,
        product_id=2835,
        reporting_enabled=False,
        reporting_sleep=0,
    ) -> None:
        self.reporting_enabled = reporting_enabled
        self.reporting_sleep = reporting_sleep
        self.controller = hid.Device(vendor_id, product_id)
        self.controller.set_nonblocking = True
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

    def notify_y_button(self) -> None:
        for observer in self._observers:
            observer_method = getattr(observer, "y_button", None)
            if callable(observer_method):
                observer_method()

    def notify_buttons(self, buttons) -> None:
        for observer in self._observers:
            for button in buttons:
                observer_method = getattr(observer, button, None)
                if callable(observer_method):
                    observer_method()

    def monitor(self) -> None:
        while True:
            report = self.controller.read(64)

            if report:
                state = XboxControllerState(report)

                # Print debug state
                if self.reporting_enabled:
                    print(state)
                    if self.reporting_sleep != 0:
                        time.sleep(self.reporting_sleep)

                # Call subscribers
                # if state.buttons.x:
                #     self.notify_x_button()

                # if state.buttons.y:
                #     self.notify_y_button()

                self.notify_buttons(state.buttons.pressed_buttons())


def print_xbox_device_info() -> None:
    for device in hid.enumerate():
        if device["product_string"] == "Xbox Wireless Controller":
            print("#" * 100)
            print(
                f"# 0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}"
            )
            print("#" * 100)
            pprint(device)


class GameObject(object):
    def __init__(self, shooting_noise="Pew", jumping_noise="boing"):
        self.shooting_noise = shooting_noise
        self.jumping_noise = jumping_noise

    def x_button(self) -> None:
        print(self.shooting_noise)

    def y_button(self) -> None:
        print(self.jumping_noise)


# gamepad = hid.device()
# gamepad.open(0x045e, 0x0b13)
# gamepad.set_nonblocking(True)

# while True:
#     report = gamepad.read(64)
#     if report:
#         print(report)

# print_xbox_device_info()


if __name__ == "__main__":
    # x = XboxController(reporting_enabled=True, reporting_sleep=0.5)
    pprint(find_hid_devices())
    x = XboxController()
    a = GameObject()
    x.attach(a)
    b = GameObject("Bang")
    x.attach(b)

    x.monitor()
