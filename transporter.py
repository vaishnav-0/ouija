import time

import serial

from constants import LETTER_MAP


class Transporter:
    COMMANDS = {
        "go": "GO",
        "reset": "RESET",
        "spin": "SPIN"
    }

    def __init__(self, port="COM3", baud=115200):
        self.serial = serial.Serial(port, baud, timeout=1)

    def write(self, text):
        self.serial.write(f"{text}\n".encode())
        self.serial.flush()

    def read_line(self):
        return self.serial.readline().decode().strip()

    def wait_for_char(self, char, timeout_seconds=180):
        start_time = time.time()

        while True:
            # Check for timeout
            if time.time() - start_time > timeout_seconds:
                print(f"Timeout: {char} not received from Arduino")
                break

            if self.serial.in_waiting > 0:
                line = self.read_line()
                print(f"Received from Arduino: {line}")
                if char in line:
                    print(f"Received {char} from Arduino")
                    break

    @staticmethod
    def _get_cords(text):
        text = "".join([c for c in text if c.isalnum()])
        text = text.upper()

        if text in LETTER_MAP:
            return [LETTER_MAP[text]]

        return [LETTER_MAP[c] for c in text]

    def write_as_coords(self, text):
        for coord in self._get_cords(text):
            self.write(f"{self.COMMANDS['go']} {coord[0]} {coord[1]}")

        self.wait_for_char("*")


if __name__ == "__main__":
    transporter = Transporter("COM4")

    while True:
        txt = input("Enter coords/text")
        if txt.startswith(":"):
            transporter.write(f"{transporter.COMMANDS['go']} {txt[1:]}")
        elif txt.startswith("!"):
            transporter.write(txt[1:].upper())
        else:
            transporter.write_as_coords(txt)
