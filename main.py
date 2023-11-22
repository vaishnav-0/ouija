import glob
import random
from time import sleep

import serial

from audio import Audio
from constants import LETTER_MAP
from mistral import Mistral

# ser = serial.Serial('COM3', 9600, timeout=1)


def send_to_serial(text):
    # ser.write(text.encode())
    # ser.flush()
    pass


def text_to_coords(answer):
    # Remove any characters other than alphabets abd numbers
    answer = "".join([c for c in answer if c.isalnum()])
    answer = answer.upper()

    if answer in LETTER_MAP:
        return [LETTER_MAP[answer]]

    return [LETTER_MAP[c] for c in answer]


def main():
    audio = Audio(silent_frames=2)

    audio.set_pre_recording(lambda: send_to_serial("SPIN"))
    audio.set_post_recording(lambda: send_to_serial("STOP"))
    audio.set_while_silent(None)

    ghosts = glob.glob("ghosts/*.txt")
    ghost = random.choice(ghosts)

    mistral = Mistral(ghost)

    while True:
        try:
            question = audio.get_transcript()
            answer = mistral(question)
            coords = text_to_coords(answer)

            for coord in coords:
                send_to_serial(",".join(map(str, coord)))
                sleep(10)

        except KeyboardInterrupt:
            break

    send_to_serial("CENTER")


if __name__ == '__main__':
    main()
